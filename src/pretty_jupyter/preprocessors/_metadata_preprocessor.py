from nbconvert.preprocessors import Preprocessor
from traitlets import CBool, CUnicode

from pretty_jupyter.magics import is_jinja_cell


class NbMetadataPreprocessor(Preprocessor):
    """
    This preprocessor merges user-defined metadata with the ones seen in notebook into one dictionary.

    This dictionary is then used for further processing.
    """
    # BASIC

    title = CUnicode(default_value="Untitled")
    """Title of the notebook."""

    toc = CBool(default_value=True)
    """If True, then TOC is generated."""

    code_folding = CUnicode(default_value="hide")
    """Settings for code folding."""

    theme = CUnicode(default_value="paper")
    """Name of the theme."""

    # OUTPUT

    output_stream_stderr = CBool(default_value=False)
    """If False, then stream stderr is omitted from the result report."""
    output_stream_stdout = CBool(default_value=True)
    """If False, then stream stdout is omitted from the result report."""
    input_jinja_markdown = CBool(default_value=False)
    """If False, then input of Jinja Markdown cells is omitted from the result report."""

    # INCLUDES

    include_plotlyjs = CBool(default_value=True)
    """If False, then the plotly.js isn't included offline in the output."""


    def __init__(self, **kw):
        # get keys that were passed: this helps to differentiate defaults and user-specified value
        self.keys_passed = set(kw)
        super().__init__(**kw)

    def preprocess(self, nb, resources):
        metadata = {
            "title": self.title,
            "toc": self.toc,
            "code_folding": self.code_folding,

            "output_stream_stderr": self.output_stream_stderr,
            "output_stream_stdout": self.output_stream_stdout,
            "input_jinja_markdown": self.input_jinja_markdown,

            "theme": self.theme
        }

        # merge specified in NbMetadataProcessor with notebook metadata
        # priority:
        # 1. Values specified by user in NbMetadataProcessor
        # 2. Values specified by user in notebook metadata
        # 3. Default values from NbMetadataProcessor

        nb_metadata = nb.metadata.copy()
        for k, v in metadata.items():
            # in class specified by user
            if k in self.keys_passed:
                nb_metadata[k] = v
                continue

            # in notebook
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
