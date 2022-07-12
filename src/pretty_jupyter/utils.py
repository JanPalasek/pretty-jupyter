def is_jinja_cell(input_str: str) -> bool:
    """
    Checks whether the input is input of a jinja cell.

    Args:
        input_str (str): Input.

    Returns:
        bool: True, if it is.
    """
    lines = input_str.splitlines()

    if len(lines) == 0:
        return False

    first_line = lines[0]
    fns = [
        lambda l: l.startswith("%%jinja"),
        lambda l: l.startswith("%%jmd")
    ]

    return any(fn(first_line) for fn in fns)