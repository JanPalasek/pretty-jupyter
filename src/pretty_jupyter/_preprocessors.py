"""
The main purpose of this package is to provide templates that make the output HTML export from
ipynb look more pretty.

"""


import re
from nbconvert.preprocessors import Preprocessor


HTML_TOKEN_FORMAT = "<span class='{token}' style='display: none;'></span>"

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
    [//]: <> (__some_token)
    ```

    Generated HTML:
    ```html
    <h2>Chapter</h2>
    <span class='__some_token' style='display: none;'></span>
    ```
    """
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type != "markdown":
            return cell, resources

        # matches markdown comments, e.g.:
        # [//]: <> (...)
        REGEX = r"\s*\[.+\]:\s*<>\s*\((.*)\)"

        all_lines = []
        for line in cell.source.splitlines():
            result = re.search(REGEX, line)
            if not result:
                all_lines.append(line)
                continue

            for gr in result.groups():
                tokens = gr.split(" ")
                tokens = [m for m in tokens if m.startswith("__")]

                new = ""
                for token in tokens:
                    new += HTML_TOKEN_FORMAT.format(token=token)
                old = line[result.span()[0]:result.span()[1]]
                line = line.replace(old, new)
            all_lines.append(line)

        # overwrite source
        cell.source = "\n".join(all_lines)
        return cell, resources

