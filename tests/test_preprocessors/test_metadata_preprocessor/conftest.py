from pathlib import Path
from unittest.mock import MagicMock, PropertyMock

import pytest
import yaml


@pytest.fixture
def fixture_dir():
    return "tests/test_preprocessors/test_metadata_preprocessor/fixture"


@pytest.fixture
def raw_cell(fixture_dir):
    cell = MagicMock(name="raw_cell")
    cell.metadata = {}
    with open(Path(fixture_dir) / "raw_cell.yaml") as file:
        type(cell).source = PropertyMock(return_value=file.read())
    type(cell).cell_type = PropertyMock(return_value="raw")

    return cell


@pytest.fixture
def jmd_cell(fixture_dir):
    cell = MagicMock(name="jmd_cell")
    cell.metadata = {}
    cell.metadata["pj_metadata"] = {"input_fold": "disable"}
    with open(Path(fixture_dir) / "jmd_cell.md") as file:
        type(cell).source = PropertyMock(return_value=file.read())
    type(cell).cell_type = PropertyMock(return_value="code")
    cell.transient = None

    output = MagicMock(name="output")
    output.metadata = {}
    type(output).output_type = PropertyMock(return_value="execute_result")
    type(output).data = {"text/markdown": []}
    type(cell).outputs = PropertyMock(return_value=[output])

    return cell


@pytest.fixture
def code_cell(fixture_dir):
    cell = MagicMock(name="code_cell")
    cell.metadata = {}
    with open(Path(fixture_dir) / "code_cell.py") as file:
        type(cell).source = PropertyMock(return_value=file.read())
    type(cell).cell_type = PropertyMock(return_value="code")
    cell.transient = None

    output = MagicMock(name="output")
    output.metadata = {}

    # outputs
    outputs = []

    output = MagicMock(name="stream_stdout")
    output.metadata = {}
    type(output).output_type = PropertyMock(return_value="stream")
    type(output).name = PropertyMock(return_value="stdout")
    type(output).data = {}
    outputs.append(output)

    output = MagicMock(name="stream_stderr")
    output.metadata = {}
    type(output).output_type = PropertyMock(return_value="stream")
    type(output).name = PropertyMock(return_value="stderr")
    type(output).data = {}
    outputs.append(output)

    output = MagicMock(name="error")
    output.metadata = {}
    type(output).output_type = PropertyMock(return_value="error")
    type(output).data = {}
    outputs.append(output)

    output = MagicMock(name="execute_result")
    output.metadata = {}
    type(output).output_type = PropertyMock(return_value="execute_result")
    type(output).data = {}
    outputs.append(output)

    type(cell).outputs = PropertyMock(return_value=outputs)

    return cell


@pytest.fixture
def nb_defaults_path(fixture_dir):
    return Path(fixture_dir) / "default_nb.yaml"


@pytest.fixture
def nb_defaults(nb_defaults_path):
    with open(nb_defaults_path) as file:
        return yaml.safe_load(nb_defaults)
