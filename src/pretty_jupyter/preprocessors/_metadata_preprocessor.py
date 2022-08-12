import copy
from datetime import date, datetime
from nbconvert.preprocessors import Preprocessor
from traitlets import Bool, Dict, CUnicode
from pretty_jupyter.utils import merge_dict
import ast

import jinja2

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
        # merge specified in NbMetadataProcessor with notebook metadata
        # priority:
        # 1. Values specified by user in NbMetadataProcessor.overrides
        # 2. Values specified by user in notebook metadata
        # 3. Default values from NbMetadataProcessor.defaults
        metadata = merge_dict(self.pj_metadata, nb.metadata.get("pj_metadata", {}).copy())
        metadata = merge_dict(metadata, self.defaults)

        # run metadata rhgouth jinja templating
        metadata_copy = copy.deepcopy(metadata)
        for m_key, m_val in filter(lambda x: x[1] is not None and isinstance(x[1], str), metadata_copy.items()):
            metadata[m_key] = self.env.from_string(m_val).render(datetime=datetime, date=date, pj_metadata=metadata_copy)

        resources["pj_metadata"] = metadata

        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        """
        Processes based on the metadata provided.
        """
        if cell.cell_type != "code":
            return cell, resources

        # PRIORITIES
        # generally more specific > less specific
        # e.g. cell-level > notebook level
        # or even cell-level output_error > cell-level output, because output_error is more specific than output generally

        general_metadata = resources["pj_metadata"]["output"]["general"]
        cell_metadata = cell.metadata.get("pj_metadata", {})

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
