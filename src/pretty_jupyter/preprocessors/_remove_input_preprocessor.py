
from nbconvert.preprocessors import Preprocessor
from traitlets import CInt

from pretty_jupyter.magics import is_jinja_cell

class RemoveInputPreprocessor(Preprocessor):
    """
    Hide some specific pretty jupyter inputs. Currently we can:

    - Remove jinja input cells.
    """
    jinja = CInt(default_value=1)
    """If larger than 0, then it removes input of jinja cells."""

    def preprocess_cell(self, cell, resources, index):
        # if jinja cells should be removed and the cell is a jinja cell => remove it
        if (self.jinja
            and cell.cell_type == "code"
            and is_jinja_cell(cell.source)
            ):
            cell.transient = {"remove_source": True}

        return cell, resources