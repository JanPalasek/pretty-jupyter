
from nbconvert.preprocessors import Preprocessor
from traitlets import CInt

class RemoveInputPreprocessor(Preprocessor):
    """
    Hide some specific pretty jupyter inputs. Currently we can:

    - Remove jinja input cells, or otherwise code cells starting with `%%jinja markdown` string.
    """
    jinja = CInt(default_value=1)
    """If larger than 0, then it removes input of jinja cells."""

    def preprocess_cell(self, cell, resources, index):
        # if cell has code type and it starts with %%jinja => hide it
        if (self.jinja
            and cell.cell_type == "code"
            and len(cell.source.splitlines()) > 0
            and cell.source.splitlines()[0].startswith("%%jinja")):
            cell.transient = {"remove_source": True}

        return cell, resources