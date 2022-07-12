"""
The main purpose of this package is to provide templates that make the output HTML export from
ipynb look more pretty.

"""


from nbconvert.preprocessors import Preprocessor
from pretty_jupyter.tokens import convert_markdown_tokens_to_html


class TokenPreprocessor(Preprocessor):
    """
    A preprocessor which tokens from MD comments and transforms them
    so they do not disappear when generating html from the markdown,
    but they are instead persisted as invisible elements.


    -----------
    Example of usage:

    Source:
    ```markdown
    ## Chapter
    [//]: <> (-.- token1 token2)
    ```

    Generated HTML:
    ```html
    <h2>Chapter</h2>
    <span class='pj-token token1 token2' style='display: none;'></span>
    ```
    """
    def preprocess(self, nb, resources):
        return super().preprocess(nb, resources)
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == "markdown":
            cell.source = convert_markdown_tokens_to_html(cell.source)
        return cell, resources
