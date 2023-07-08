import copy
import warnings
from datetime import date, datetime
from pathlib import Path

import jinja2
import nbconvert
import pkg_resources
import yaml
from cerberus import Validator
from nbconvert.preprocessors import Preprocessor
from packaging import version
from traitlets import Dict

from pretty_jupyter.constants import (
    AVAILABLE_THEMES,
    CONFIG_DIR,
    DEPRECATED_METADATA_MSG_FORMAT,
    METADATA_ERROR_FORMAT,
)
from pretty_jupyter.magics import is_jinja_cell
from pretty_jupyter.tokens import read_code_metadata_token, read_markdown_metadata_token
from pretty_jupyter.utils import merge_dict

_DEPRECATED_ATTRIBUTES = ["title", "theme", "toc", "code_folding"]
_DEPRECATED_ATTRIBUTES_VERSION = "2.0.0"


class NbMetadataPreprocessor(Preprocessor):
    """
    This preprocessor merges user-defined metadata with the ones seen in notebook into one dictionary.
    The result metadata will be located in `resources["metadata"]`.

    This dictionary is then used for further processing.
    """

    pj_metadata = Dict(default_value={})
    """
    Dictionary with all values to override the defaults. Note that per_key_trait is not an exhaustive list, you can define your own new override.
    """

    nb_spec_path = Path(CONFIG_DIR) / "metadata/nb_spec.yaml"
    cell_spec_path = Path(CONFIG_DIR) / "metadata/cell_spec.yaml"
    nb_defaults_path = Path(CONFIG_DIR) / "metadata/nb_defaults.yaml"

    def __init__(self, **kw):
        if "pj_metadata" in kw and isinstance(kw["pj_metadata"], str):
            # convert to dictionary
            kw["pj_metadata"] = yaml.safe_load(kw["pj_metadata"])

        super().__init__(**kw)

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))

        with open(self.nb_spec_path) as file:
            nb_spec = yaml.safe_load(file.read())
        self.nb_validator = Validator(nb_spec, allow_unknown=True)

        with open(self.cell_spec_path) as file:
            cell_spec = yaml.safe_load(file.read())
        self.cell_validator = Validator(cell_spec)

        with open(self.nb_defaults_path) as file:
            nb_defaults = yaml.safe_load(file.read())
        self.defaults = nb_defaults

    def preprocess(self, nb, resources):
        # deprecation warnings to help users fix their error
        deprecated_attrs = [a for a in _DEPRECATED_ATTRIBUTES if a in nb.metadata]
        if len(deprecated_attrs) > 0:
            warnings.warn(
                DEPRECATED_METADATA_MSG_FORMAT.format(
                    attributes=", ".join(deprecated_attrs), version=_DEPRECATED_ATTRIBUTES_VERSION
                ),
                category=DeprecationWarning,
            )

        # temporarily store nb metadata to resources to be accessible in cell
        resources["__pj_metadata"] = nb.metadata.get("pj_metadata", {})
        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        """
        Processes based on the metadata provided.

        PRIORITIES: generally more specific > less specific

        - e.g. cell-level > notebook level
        - e.g. cell-level output_error > cell-level output because output_error is more specific than output generally
        """
        if index == 0:
            self._synchronize_notebook_metadata(cell, resources)

        self._synchronize_cell_metadata(cell)
        if cell.cell_type == "markdown":
            cell, resources = self._preprocess_markdown_cell(cell, resources, index)
        if cell.cell_type == "code":
            cell, resources = self._preprocess_code_cell(cell, resources, index)

        return cell, resources

    def _synchronize_notebook_metadata(self, cell, resources):
        nb_metadata = resources.get("__pj_metadata", {})
        src_metadata = {}
        if cell.cell_type == "raw":
            try:
                src_metadata = yaml.safe_load(cell.source)
            except Exception as exc:
                raise ValueError(
                    "An error happend when trying to parse first cell of the notebook with type raw.",
                    exc,
                )

            remove_cell_input(cell)

        if len(nb_metadata) > 0 and len(src_metadata) > 0:
            warnings.warn(
                "Notebook-level metadata are defined both in the source and in the notebook's metadata. Please remove one of them."
            )

        metadata = src_metadata if len(src_metadata) > 0 else nb_metadata

        # validate metadata
        is_valid = self.nb_validator.validate(metadata)
        if not is_valid:
            raise ValueError(METADATA_ERROR_FORMAT.format(error=str(self.nb_validator.errors)))

        # merge specified in NbMetadataProcessor with notebook metadata
        # priority:
        # 1. Values specified by user in NbMetadataProcessor.overrides
        # 2. Values specified by user in notebook metadata
        # 3. Default values from NbMetadataProcessor.defaults
        metadata = merge_dict(self.pj_metadata, metadata)
        metadata = merge_dict(metadata, self.defaults)

        # run metadata through jinja templating
        metadata_copy = copy.deepcopy(metadata)
        for m_key, m_val in filter(
            lambda x: x[1] is not None and isinstance(x[1], str), metadata_copy.items()
        ):
            metadata[m_key] = self.env.from_string(m_val).render(
                datetime=datetime, date=date, pj_metadata=metadata_copy
            )

        resources["pj_metadata"] = metadata

        del resources["__pj_metadata"]

    def _synchronize_cell_metadata(self, cell):
        """
        Synchronizes cell metadata from tokens and metadata into one dictionary and stores it into cell.metadata.

        Args:
            cell: Cell.
        """
        src_cell_metadata = None
        source_lines = cell.source.splitlines()
        is_empty = len(source_lines) == 0
        # if cell is jinja markdown
        if not is_empty and cell.cell_type == "code" and is_jinja_cell(cell.source):
            # read src_cell_metadata from the second line (after jmd), if the file has two lines
            if len(source_lines) >= 2:
                src_cell_metadata = read_markdown_metadata_token(source_lines[1])
        elif not is_empty and cell.cell_type == "code":
            src_cell_metadata = read_code_metadata_token(source_lines[0])
        elif not is_empty and cell.cell_type == "markdown":
            src_cell_metadata = read_markdown_metadata_token(source_lines[0])

        # if nothing was read, just assign blank
        if src_cell_metadata is None:
            src_cell_metadata = {}

        # cell metadata from metadata
        nb_cell_metadata = cell.metadata.get("pj_metadata", {})

        if len(src_cell_metadata) > 0 and len(nb_cell_metadata) > 0:
            msg = "Metadata for this cell were specified both in notebook's metadata and in the cell's code. Printing parts of cell's source code to help find the issue."
            msg += f"\nFirst 30 characters: {cell.source[:30]}"
            warnings.warn(msg)

        cell_metadata = src_cell_metadata if len(src_cell_metadata) > 0 else nb_cell_metadata

        if not self.cell_validator.validate(cell_metadata):
            raise ValueError(METADATA_ERROR_FORMAT.format(error=str(self.cell_validator.errors)))

        # store it to the metadata
        cell.metadata["pj_metadata"] = cell_metadata

    def _preprocess_markdown_cell(self, cell, resources, index):
        return cell, resources

    def _preprocess_code_cell(self, cell, resources, index):
        # if metadata specify that input shouldnt be enabled => remove it
        if not is_input_enabled(cell, resources):
            remove_cell_input(cell)

        for i, output in reversed(list(enumerate(cell.outputs))):
            if not is_output_enabled(cell, resources, output):
                cell.outputs.pop(i)

        return cell, resources


class HtmlNbMetadataPreprocessor(NbMetadataPreprocessor):
    def preprocess(self, nb, resources):
        resources["pj_available_themes"] = AVAILABLE_THEMES
        return super().preprocess(nb, resources)

    def _preprocess_code_cell(self, cell, resources, index):
        cell.metadata["pj_metadata"]["input_fold"] = get_code_folding_value(cell, resources)

        return super()._preprocess_code_cell(cell, resources, index)


def remove_cell_input(cell):
    # keep compatibility for version < 7
    if version.parse(nbconvert.__version__) >= version.parse("7.0.0"):
        cell.metadata["transient"] = {"remove_source": True}
    else:
        cell.transient = {"remove_source": True}


def is_output_enabled(cell, resources, output):
    cell_metadata = cell.metadata["pj_metadata"]
    nb_metadata = resources["pj_metadata"]["output"]["general"]

    def is_stdout(output):
        return output.output_type == "stream" and output.name == "stdout"

    def is_error(output):
        return output.output_type == "error" or (
            output.output_type == "stream" and output.name == "stderr"
        )

    # PRIORITY
    # cell > notebook-level, stdout > output (similarly stderr)
    # we will set a default as the most general setting and then progressively overwrite it by more specific settings
    # least specific: notebook-level output
    # most specific: stdout/stderr cell output

    is_enabled = nb_metadata["output"]
    # NOTEBOOK-LEVEL
    if is_stdout(output):
        is_enabled = nb_metadata["output_stdout"]
    if is_error(output):
        is_enabled = nb_metadata["output_error"]

    # CELL-LEVEL
    if "output" in cell_metadata:
        is_enabled = cell_metadata["output"]
    if is_stdout(output) and "output_stdout" in cell_metadata:
        is_enabled = cell_metadata["output_stdout"]
    # STDERR
    if is_error(output) and "output_error" in cell_metadata:
        is_enabled = cell_metadata["output_error"]

    return is_enabled


def is_input_enabled(cell, resources):
    cell_metadata = cell.metadata["pj_metadata"]
    nb_metadata = resources["pj_metadata"]["output"]["general"]

    is_enabled = nb_metadata["input"]
    if is_jinja_cell(cell.source):
        is_enabled = nb_metadata["input_jinja"]

    # if value was specified in cell metadata => use that
    if "input" in cell_metadata:
        is_enabled = cell_metadata["input"]

    return is_enabled


def get_code_folding_value(cell, resources):
    cell_metadata = cell.metadata["pj_metadata"]
    nb_metadata = resources["pj_metadata"]["output"]["html"]

    code_folding = nb_metadata["code_folding"]
    if "input_fold" in cell_metadata:
        code_folding = cell_metadata["input_fold"]
    value = f"fold-{code_folding}"
    return value
