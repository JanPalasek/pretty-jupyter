MARKDOWN_TOKEN_REGEX = r"\s*\[.+\]:\s*<>\s*\(-\.-\s+(.*)\)"
"""
Regex to match markdown tokens. The tokens are special sequences in markdown that invoke special behaviour, e.g. tabsets. Example of some tokens:

```
[//]: <> (-.- token1 token2 token3)
```
"""

HTML_TOKEN_REGEX = "<span class='pj-token' style='display: none;'>.*<\/span>"

HTML_TOKEN_FORMAT = "<span class='pj-token' style='display: none;'>{tokens}</span>"
"""
What markdown tokens get translated to.
"""

TOKEN_SEP = "|O_O|"
"""Separator for multiple tokens"""

CODE_METADATA_TOKEN_REGEX = r"^\s*#\s+-\.-\|pj_metadata\s+(.*)$"
"""
Regex to match markdown metadata tokens.

```
# -.-|pj_metadata { "input": false, "output": true }
```
"""

MARKDOWN_METADATA_TOKEN_REGEX = r"^\s*\[.+\]:\s*<>\s*\(-\.-\|pj_metadata\s+(.*)\)$"
"""
Regex to match markdown metadata tokens.

```
[//]: (-.-|pj_metadata { "input": true, "output": false })
```
"""
