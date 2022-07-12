import re

_MARKDOWN_TOKEN_REGEX = r"\s*\[.+\]:\s*<>\s*\(-.-\s+(.*)\)"
"""
Regex to match tokens. The tokens are special sequences in markdown that invoke special behaviour, e.g. tabsets. Example of some tokens:

```
[//]: <> (-.- token1 token2 token3)
```
"""

_HTML_TOKEN_FORMAT = "<span class='pj-token {tokens}' style='display: none;'></span>"
"""
What markdown tokens get translated to.
"""

def convert_markdown_tokens_to_html(input_str: str) -> str:
    """
    Processes input markdown string, converting all tokens from markdown token format
    to HTML token format.

    Args:
        input_str (str): Input string in markdown.

    Returns:
        str: Output string in markdown with tokens in HTML format.
    """
    all_lines = []
    for line in input_str.splitlines():
        result = re.search(_MARKDOWN_TOKEN_REGEX, line)
        if not result:
            all_lines.append(line)
            continue

        for gr in result.groups():
            # get tokens by splitting by any whitespace and taking non-empty entries
            tokens = filter(lambda x: len(x) > 0, (m.strip() for m in gr.split()))

            # join them together and create html token out of them
            token_str = " ".join(tokens)
            html = _HTML_TOKEN_FORMAT.format(tokens=token_str)

            # replace the md tokens by html tokens
            markdown = line[result.span()[0]:result.span()[1]]
            line = line.replace(markdown, html)
        all_lines.append(line)

    # output is still in md, but token
    output = "\n".join(all_lines)
    return output