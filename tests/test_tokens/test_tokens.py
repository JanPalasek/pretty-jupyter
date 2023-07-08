from pretty_jupyter.tokens import convert_markdown_tokens_to_html


def test_convert_markdown_tokens_to_html(input_str, expected_str):
    actual_str = convert_markdown_tokens_to_html(input_str)

    assert actual_str == expected_str, "Expected string is different than the actual."
