MARKDOWN_TOKEN_REGEX = r"\s*\[.+\]:\s*<>\s*\(-.-\s+(.*)\)"
"""
Regex to match tokens. The tokens are special sequences in markdown that invoke special behaviour, e.g. tabsets. Example of some tokens:

```
[//]: <> (-.- token1 token2 token3)
```
"""

HTML_TOKEN_FORMAT = "<span class='pj-token' style='display: none;'>{tokens}</span>"
"""
What markdown tokens get translated to.
"""

TOKEN_SEP = "|O_O|"
"""Separator for multiple tokens"""
