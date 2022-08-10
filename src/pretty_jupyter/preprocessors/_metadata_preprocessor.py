from nbconvert.preprocessors import Preprocessor
from traitlets import Bool, Dict, CUnicode
from pretty_jupyter.utils import merge_dict
import ast

from pretty_jupyter.magics import is_jinja_cell


class NbMetadataPreprocessor(Preprocessor):
    """
    This preprocessor merges user-defined metadata with the ones seen in notebook into one dictionary.
    The result metadata will be located in `resources["metadata"]`.

    This dictionary is then used for further processing.
    """

    defaults = {
        "title": "Untitled",
        "html": {
            "toc": True,
            "code_folding": True,
            "theme": "paper",
            "include_plotlyjs": True
        },
        "output_stream_stderr": False,
        "output_stream_stdout": True,
        "input_jinja_markdown": False,
    }

    overrides = Dict(default_value={})
    """
    Dictionary with all values to override the defaults. Note that per_key_trait is not an exhaustive list, you can define your own new override.
    """

    def __init__(self, **kw):
        if "overrides" in kw and isinstance(kw["overrides"], str):
            # convert to dictionary
            kw["overrides"] = ast.literal_eval(kw["overrides"])

        super().__init__(**kw)

    def preprocess(self, nb, resources):
        metadata = merge_dict(self.overrides, self.defaults)

        # merge specified in NbMetadataProcessor with notebook metadata
        # priority:
        # 1. Values specified by user in NbMetadataProcessor.overrides
        # 2. Values specified by user in notebook metadata
        # 3. Default values from NbMetadataProcessor.defaults

        nb_metadata = nb.metadata.copy()
        for k, v in metadata.items():
            # if specified by user
            if k in self.overrides:
                nb_metadata[k] = v
                continue

            # if specified in notebook
            if k in nb_metadata:
                continue

            # only in defaults
            nb_metadata[k] = v

        resources["nb_metadata"] = nb_metadata

        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        """
        Processes based on the metadata provided.
        """
        if cell.cell_type != "code":
            return cell, resources

        metadata = resources["nb_metadata"]

        # process jinja markdown
        if not metadata["input_jinja_markdown"] and is_jinja_cell(cell.source):
            cell.transient = {"remove_source": True}

        # process stderr, stdout
        if len(cell.outputs) > 0:
            for i, output in enumerate(cell.outputs):
                # stderr
                if not metadata["output_stream_stderr"] and output.output_type == "stream" and output.name == "stderr":
                    cell.outputs.pop(i)
                # stdout
                elif not metadata["output_stream_stdout"] and output.output_type == "stream" and output.name == "stdout":
                    cell.outputs.pop(i)
        
        return cell, resources
