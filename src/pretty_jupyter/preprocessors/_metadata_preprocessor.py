import copy
from datetime import date, datetime
import json
from nbconvert.preprocessors import Preprocessor
from traitlets import Bool, Dict, CUnicode
from pretty_jupyter.utils import merge_dict
import ast

import jinja2

from pretty_jupyter.tokens import read_code_metadata_token, read_markdown_metadata_token
from pretty_jupyter.magics import is_jinja_cell


class NbMetadataPreprocessor(Preprocessor):
    """
    This preprocessor merges user-defined metadata with the ones seen in notebook into one dictionary.
    The result metadata will be located in `resources["metadata"]`.

    This dictionary is then used for further processing.
    """

    defaults = {
        "title": "Untitled",
        "output": {
            "general": {
                "input": True,
                "input_jmd": False,
                "output": True,
                "output_error": False,
            },
            "html": {
                "toc": True,
                "toc_depth": 3,
                "toc_collapsed": True,
                "toc_smooth_scroll": True,
                "number_sections": False,
                "code_folding": "hide",
                "tabset": True,
                "theme": "paper",
                "include_plotlyjs": True
            },
            "pdf": {
                "toc": True,
                "toc_depth": 3,
                "language": "english"
            }
        },
    }

    pj_metadata = Dict(default_value={})
    """
    Dictionary with all values to override the defaults. Note that per_key_trait is not an exhaustive list, you can define your own new override.
    """

    def __init__(self, **kw):
        if "pj_metadata" in kw and isinstance(kw["pj_metadata"], str):
            # convert to dictionary
            kw["pj_metadata"] = ast.literal_eval(kw["pj_metadata"])

        super().__init__(**kw)

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    def preprocess(self, nb, resources):
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
        self._synchronize_cell_metadata(cell)

        if index == 0:
            pj_metadata = json.loads(cell.source) if cell.cell_type == "raw" else resources["__pj_metadata"]
            self._synchronize_notebook_metadata(resources, pj_metadata)
            del resources["__pj_metadata"]
        elif cell.cell_type == "markdown":
            cell, resources = self._preprocess_markdown_cell(cell, resources, index)
        if cell.cell_type == "code":
            cell, resources = self._preprocess_code_cell(cell, resources, index)
        
        return cell, resources

    def _synchronize_notebook_metadata(self, resources, pj_metadata):
        # merge specified in NbMetadataProcessor with notebook metadata
        # priority:
        # 1. Values specified by user in NbMetadataProcessor.overrides
        # 2. Values specified by user in notebook metadata
        # 3. Default values from NbMetadataProcessor.defaults
        metadata = merge_dict(self.pj_metadata, pj_metadata)
        metadata = merge_dict(metadata, self.defaults)

        # run metadata through jinja templating
        metadata_copy = copy.deepcopy(metadata)
        for m_key, m_val in filter(lambda x: x[1] is not None and isinstance(x[1], str), metadata_copy.items()):
            metadata[m_key] = self.env.from_string(m_val).render(datetime=datetime, date=date, pj_metadata=metadata_copy)

        resources["pj_metadata"] = metadata

    def _synchronize_cell_metadata(self, cell):
        """
        Synchronizes cell metadata from tokens and metadata into one dictionary and stores it into cell.metadata.

        Args:
            cell: Cell.
        """
        cell_metadata = None

        source_lines = cell.source.splitlines()
        is_empty = len(source_lines) == 0
        if not is_empty and cell.cell_type == "code" and is_jinja_cell(cell.source):
            cell_metadata = read_markdown_metadata_token(source_lines[1])
        elif not is_empty and cell.cell_type == "code":
            cell_metadata = read_code_metadata_token(source_lines[0])
        elif cell.cell_type == "markdown" and not is_empty:
            cell_metadata = read_markdown_metadata_token(source_lines[0])

        # if cell metadata hasn't been found in the code, try to take it from cell metadata
        if cell_metadata is None:
            cell_metadata = cell.metadata.get("pj_metadata", {})

        # store it to the metadata
        cell.metadata["pj_metadata"] = cell_metadata

    def _preprocess_markdown_cell(self, cell, resources, index):
        return cell, resources

    def _preprocess_code_cell(self, cell, resources, index):
        cell_metadata = cell.metadata["pj_metadata"]
        general_metadata = resources["pj_metadata"]["output"]["general"]

        #########
        # INPUT #
        #########
        input_enabled = general_metadata["input"]
        # if this cell is jinja markdown and metadata specify to turn it off => set it as turn off
        if is_jinja_cell(cell.source):
            input_enabled = general_metadata["input_jmd"]
        # if value was specified in cell metadata => use that
        if "input" in cell_metadata:
            input_enabled = cell_metadata["input"]
        # if input is not enabled => remove 
        if not input_enabled:
            cell.transient = {"remove_source": True}

        ##########
        # OUTPUT #
        ##########
        output_enabled = general_metadata["output"]
        # process stderr, stdout
        if len(cell.outputs) > 0:
            for i, output in enumerate(cell.outputs):
                ith_output_enabled = output_enabled
                # if this output is an error output => write out output is output error is true
                if output.output_type == "stream" and output.name == "stderr":
                    ith_output_enabled = general_metadata["output_error"]
                # if value was specified in cell metadata => use that
                if "output" in cell_metadata:
                    ith_output_enabled = cell_metadata["output"]
                if "output_error" in cell_metadata and output.output_type == "stream" and output.name == "stderr":
                    ith_output_enabled = cell_metadata["output_error"]
                # output not enabled => remove
                if not ith_output_enabled:
                    cell.outputs.pop(i)
        
        return cell, resources


class HtmlNbMetadataPreprocessor(NbMetadataPreprocessor):
    def _preprocess_code_cell(self, cell, resources, index):
        cell_metadata = cell.metadata["pj_metadata"]

        ################
        # CODE-FOLDING #
        ################
        html_metadata = resources["pj_metadata"]["output"]["html"]
        code_folding = html_metadata["code_folding"]
        if "input_fold" in cell_metadata:
            code_folding = cell_metadata["input_fold"]
        cell_metadata["input_fold"] = f"fold-{code_folding}"

        # assign value to the cell metadata
        cell.metadata["pj_metadata"] = cell_metadata

        return super()._preprocess_code_cell(cell, resources, index)
