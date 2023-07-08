"""
The main purpose of this package is to provide templates that make the output HTML export from
ipynb look more pretty.

"""


import re

from nbconvert.preprocessors import Preprocessor

from pretty_jupyter.constants import HTML_TOKEN_REGEX, TOKEN_SEP
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
        resources["token_sep"] = TOKEN_SEP

        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == "markdown":
            cell.source = convert_markdown_tokens_to_html(cell.source)
        return cell, resources


class TokenCleaningPreprocessor(Preprocessor):
    """
    Deletes tokens from cell outputs.
    """

    formats = ["text/markdown", "text/html"]

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == "code":
            for i, output in enumerate(cell.outputs):
                if not "data" in output:
                    continue

                output_data = output["data"]

                # get cell format
                cell_format = None
                for f in self.formats:
                    if f in output_data:
                        cell_format = f
                        break

                # if none matched => ignore this cell
                if cell_format is None:
                    continue

                output_data[f] = re.sub(pattern=HTML_TOKEN_REGEX, repl="", string=output_data[f])

        return cell, resources
