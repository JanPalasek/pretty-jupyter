
from nbconvert.preprocessors import Preprocessor
from traitlets import CInt
import functools


class RemoveOutputPreprocessor(Preprocessor):
    """
    Removes specified outputs based on its parameters.
    """

    stream_stdout = CInt(default_value=0)
    """If non-zero, then all streams of type std_out are removed from the list of cell's outputs."""
    stream_stderr = CInt(default_value=1)
    """If non-zero, then all streams of type std_err are removed from the list of cell's outputs."""
    output_error = CInt(default_value=1)
    """If non-zero, then all outputs of type error are removed from the list of cell's outputs."""

    def __init__(self, **kw):
        super().__init__(**kw)

        # define condition functions validating, whether given output is to be removed or not
        self.conditions_fns = [
            # remove stdout
            functools.partial(
                lambda output, stream_stdout: stream_stdout and output.output_type == "stream" and output.name == "stdout",
                stream_stdout=self.stream_stdout),
            # remove stderr
            functools.partial(
                lambda output, stream_stderr: stream_stderr and output.output_type == "stream" and output.name == "stderr",
                stream_stderr=self.stream_stderr),  
            # remove output of type error          
            functools.partial(
                lambda output, output_error: output_error and output.output_type == "error",
                output_error=self.output_error),                   
        ]

    def preprocess_cell(self, cell, resources, index):
        # if cell has code type and it starts with %%jinja => hide it
        if not (cell.cell_type == "code" and len(cell.outputs) > 0):
            return cell, resources

        for i, output in enumerate(cell.outputs):
            if any(fn(output) for fn in self.conditions_fns):
                cell.outputs.pop(i)

        return cell, resources