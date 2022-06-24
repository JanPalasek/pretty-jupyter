
from nbconvert.preprocessors import Preprocessor
from traitlets import CInt

class RemoveInputPreprocessor(Preprocessor):
    """
    Hide some specific pretty jupyter inputs. Currently we can:

    - Remove jmarkdown input cells, or otherwise code cells starting with `%%jmarkdown` string.
    """
    jmarkdown = CInt(default_value=1)
    """If larger than 0, then it removes input of jmarkdown cells."""

    def preprocess_cell(self, cell, resources, index):
        # if cell has code type and it starts with %%jmarkdown => hide it
        if (self.jmarkdown
            and cell.cell_type == "code"
            and cell.source.splitlines()[0].startswith("%%jmarkdown")):
            cell.transient = {"remove_source": True}

        return cell, resources