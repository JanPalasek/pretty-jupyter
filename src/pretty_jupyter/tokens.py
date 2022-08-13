import json
import re
from pretty_jupyter.constants import CODE_METADATA_TOKEN_REGEX, MARKDOWN_METADATA_TOKEN_REGEX, MARKDOWN_TOKEN_REGEX, HTML_TOKEN_FORMAT, TOKEN_SEP


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
        result = re.search(MARKDOWN_TOKEN_REGEX, line)
        if not result:
            all_lines.append(line)
            continue

        for gr in result.groups():
            # get tokens by splitting by any whitespace and taking non-empty entries
            tokens = filter(lambda x: len(x) > 0, (m.strip() for m in gr.split()))

            # join them together and create html token out of them
            token_str = TOKEN_SEP.join(tokens)
            html = HTML_TOKEN_FORMAT.format(tokens=token_str)

            # replace the md tokens by html tokens
            markdown = line[result.span()[0]:result.span()[1]]
            line = line.replace(markdown, html)
        all_lines.append(line)

    # output is still in md, but token
    output = "\n".join(all_lines)
    return output

def read_code_metadata_token(input_str: str) -> dict:
    lines = input_str.splitlines()
    if len(lines) == 0:
        return None

    line = lines[0]

    # parse token
    result = re.search(CODE_METADATA_TOKEN_REGEX, line)

    if not result:
        return None

    if len(result.groups()) == 0:
        return None

    return json.loads(result.groups()[0])

def read_markdown_metadata_token(input_str: str):
    lines = input_str.splitlines()
    if len(lines) == 0:
        return None

    line = lines[0]

    # parse token
    result = re.search(MARKDOWN_METADATA_TOKEN_REGEX, line)

    if not result:
        return None

    if len(result.groups()) == 0:
        return None

    return json.loads(result.groups()[0])