from click.testing import CliRunner
import pytest
from pretty_jupyter.console import cli
import os

@pytest.fixture
def input_path():
    return "tests/fixture/notebook.ipynb"


def test_nbconvert(input_path, tmpdir):
    out_path = os.path.join(tmpdir, "actual.html")

    runner = CliRunner()
    result = runner.invoke(cli, ["nbconvert", input_path, "--out", out_path])
    
    assert result.exit_code == 0

    # TODO: transform to selenium
    assert os.path.exists(out_path)
