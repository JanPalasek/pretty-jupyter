from pathlib import Path
from unittest.mock import MagicMock

import nbconvert
import pytest
import yaml
from packaging import version

from pretty_jupyter.preprocessors import HtmlNbMetadataPreprocessor, NbMetadataPreprocessor


@pytest.fixture
def expected_raw_cell(fixture_dir):
    with open(Path(fixture_dir) / "expected_test_raw.yaml") as file:
        return yaml.safe_load(file.read())


def test_preprocess_raw_cell(raw_cell, nb_defaults_path, expected_raw_cell):
    NbMetadataPreprocessor.nb_defaults_path = nb_defaults_path
    override_config = "{ output: { general: { input: false } } }"
    preprocessor = NbMetadataPreprocessor(pj_metadata=override_config)

    nb = MagicMock(name="nb")
    nb.metadata = {}
    resources = {}

    preprocessor.preprocess(nb, resources)

    index = 0
    cell, resources = preprocessor.preprocess_cell(raw_cell, resources, index)

    assert resources["pj_metadata"] == expected_raw_cell


def test_preprocess_jmd_cell(jmd_cell, nb_defaults_path):
    HtmlNbMetadataPreprocessor.nb_defaults_path = nb_defaults_path
    preprocessor = HtmlNbMetadataPreprocessor()

    resources = {}
    resources["pj_metadata"] = preprocessor.defaults

    # must raise warning because cell has specified metadata both in code and nb metadata
    # cell metadata have priority tho and nb metadata for the cell are ignored
    with pytest.warns(UserWarning):
        cell, resources = preprocessor.preprocess_cell(jmd_cell, resources, index=3)

    assert cell.metadata["pj_metadata"] == {
        "input": False,
        "output": False,
        "input_fold": "fold-show",
        "output_error": True,
    }
    if version.parse(nbconvert.__version__) >= version.parse("7.0.0"):
        assert cell.metadata["transient"] == {"remove_source": True}
    else:
        assert cell.transient == {"remove_source": True}
    assert len(cell.outputs) == 0


def test_preprocess_code_cell(code_cell, nb_defaults_path):
    HtmlNbMetadataPreprocessor.nb_defaults_path = nb_defaults_path
    preprocessor = HtmlNbMetadataPreprocessor()
    resources = {}
    resources["pj_metadata"] = preprocessor.defaults

    cell, resources = preprocessor.preprocess_cell(code_cell, resources, index=2)

    assert cell.transient is None
    assert len(cell.outputs) == 1
    assert cell.outputs[0].output_type == "execute_result"
