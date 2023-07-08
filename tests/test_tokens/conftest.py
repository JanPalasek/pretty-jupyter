import pytest


@pytest.fixture
def input_str():
    with open("tests/test_tokens/fixture/input.md", "r") as file:
        return file.read()


@pytest.fixture
def expected_str():
    with open("tests/test_tokens/fixture/expected.md", "r") as file:
        return file.read()
