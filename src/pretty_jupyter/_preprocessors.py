"""
The main purpose of this package is to provide templates that make the output HTML export from
ipynb look more pretty.

"""


from hashlib import md5
import re
from nbconvert.preprocessors import Preprocessor


TOKEN_REGEX = r"\s*\[.+\]:\s*<>\s*\(-.-\s+(.*)\)"
"""
Regex to match tokens. The tokens are special sequences in markdown that invoke special behaviour, e.g. tabsets. Example of some tokens:

```
[//]: <> (-.- token1 token2 token3)
```
"""

HTML_TOKEN_FORMAT = "<span class='pretty-jupyter-token {tokens}' style='display: none;'></span>"
"""
What markdown tokens get translated to.
"""


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
    <span class='pretty-jupyter-token token1 token2' style='display: none;'></span>
    ```
    """
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type != "markdown":
            return cell, resources

        all_lines = []
        for line in cell.source.splitlines():
            result = re.search(TOKEN_REGEX, line)
            if not result:
                all_lines.append(line)
                continue

            for gr in result.groups():
                tokens = [m.strip() for m in gr.split(" ")]

                html = HTML_TOKEN_FORMAT.format(tokens=" ".join(tokens))

                markdown = line[result.span()[0]:result.span()[1]]
                line = line.replace(markdown, html)
            all_lines.append(line)

        # overwrite source
        cell.source = "\n".join(all_lines)
        return cell, resources

