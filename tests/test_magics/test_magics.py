from unittest.mock import MagicMock, PropertyMock
from pretty_jupyter.magics import JMarkdownMagics

def test_jmarkdown():
    shell_mock = MagicMock(name="shell", spec=["user_ns", "user_ns_hidden"])
    type(shell_mock).user_ns = PropertyMock(
        name="user_ns",
        return_value={"a": 15}
        )
    jmarkdown = JMarkdownMagics(shell_mock)

    with open("tests/test_magics/fixture/input_jmarkdown.md") as file:
        input_str = file.read()
    actual_str = jmarkdown.jmarkdown(
        line=input_str.splitlines()[0],
        cell="\n".join(input_str.splitlines()[1:])
        ).data

    with open("tests/test_magics/fixture/expected_jmarkdown.md") as file:
        expected_str = file.read()

    assert actual_str == expected_str, "Expected string is different than the actual."