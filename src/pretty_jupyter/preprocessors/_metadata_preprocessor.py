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
        resources["pj_metadata"] = self._get_notebook_metadata(nb.metadata.get("pj_metadata", {}).copy())

        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        """
        Processes based on the metadata provided.

        PRIORITIES: generally more specific > less specific

        - e.g. cell-level > notebook level
        - e.g. cell-level output_error > cell-level output because output_error is more specific than output generally
        """
        # if it is first cell and it is of type raw => we load notebook-level metadata from there
        if cell.cell_type == "raw" and index == 0:
            self._preprocess_raw_cell(cell, resources, index)
        elif cell.cell_type == "markdown":
            cell, resources = self._preprocess_markdown_cell(cell, resources, index)
        if cell.cell_type == "code":
            cell, resources = self._preprocess_code_cell(cell, resources, index)
        
        return cell, resources

    def _get_notebook_metadata(self, pj_metadata):
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

        return metadata

    def _preprocess_raw_cell(self, cell, resources, index):
        cell.transient = {"remove_source": True}

        # load metadata
        pj_metadata = json.loads(cell.source)
        resources["pj_metadata"] = self._get_notebook_metadata(pj_metadata)

    def _get_code_cell_metadata(self, cell):
        cell_metadata = None

        source_lines = cell.source.splitlines()
        if len(source_lines) > 0 and is_jinja_cell(cell.source):
            # source without the first line (with %%jmd)
            cell_metadata = read_markdown_metadata_token("\n".join(source_lines[1:]))
        elif len(source_lines) > 0:
            # compute cell metadata
            cell_metadata = read_code_metadata_token(cell.source)

        # if cell metadata hasn't been found in the code, try to take it from cell metadata
        if cell_metadata is None:
            cell_metadata = cell.metadata.get("pj_metadata", {})

        return cell_metadata

    def _preprocess_markdown_cell(self, cell, resources, index):
        return cell, resources

    def _preprocess_code_cell(self, cell, resources, index):
        cell_metadata = self._get_code_cell_metadata(cell)
        general_metadata = resources["pj_metadata"]["output"]["general"]

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

                if not ith_output_enabled:
                    cell.outputs.pop(i)
        
        return cell, resources
