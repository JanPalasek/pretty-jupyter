import pkg_resources

MARKDOWN_TOKEN_REGEX = r"\s*\[.+\]:\s*(?:(?:<>)|#)\s*\(-\.-\s+(.*)\)"
"""
Regex to match markdown tokens. The tokens are special sequences in markdown that invoke special behaviour, e.g. tabsets. Example of some tokens:

```markdown
[//]: <> (-.- token1 token2 token3)
[//]: # (-.- token1 token2 token3)
```
"""


HTML_TOKEN_REGEX = "<span class='pj-token' style='display: none;'>.*<\/span>"
"""
Regex to match html tokens.
"""

HTML_TOKEN_FORMAT = "<span class='pj-token' style='display: none;'>{tokens}</span>"
"""
What markdown tokens get translated to.
"""

TOKEN_SEP = "|O_O|"
"""Separator for multiple tokens"""

CODE_METADATA_TOKEN_REGEX = r"^\s*#\s+-\.-\|m\s+(.*)$"
"""
Regex to match markdown metadata tokens.

```python
# -.-|m { "input": false, "output": true }
```
"""

MARKDOWN_METADATA_TOKEN_REGEX = r"^\s*\[.+\]:\s*(?:(?:<>)|#)\s*\(-\.-\|m\s+(.*)\)\s*$"
"""
Regex to match markdown metadata tokens.

```markdown
[//]: # (-.-|m { "input": true, "output": false })
[//]: <> (-.-|m { "input": true, "output": false })
```
"""

CONFIG_DIR = pkg_resources.resource_filename("pretty_jupyter", "config")

AVAILABLE_THEMES = [
    "bootstrap",
    "cerulean",
    "cosmo",
    "cyborg",
    "darkly",
    "flatly",
    "journal",
    "lumen",
    "paper",
    "readable",
    "sandstone",
    "simplex",
    "slate",
    "spacelab",
    "superhero",
    "united",
    "yeti",
]
"""
List of all available local themes that can be specified in the `theme` html metadata.
"""

DEPRECATED_METADATA_MSG_FORMAT = "Specifying attributes '{attributes}' in this position to notebook metadata is deprecated since {version}. Please consider reading changes in this version.\n"
METADATA_ERROR_FORMAT = "An error occured when validating cell metadata. Error attributes in the metadata were the following:\n{error}"
