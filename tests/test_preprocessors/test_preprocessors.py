import pytest
from unittest.mock import MagicMock, PropertyMock
from pretty_jupyter.preprocessors import NbMetadataPreprocessor


# @pytest.fixture(params=[
#     ("tests/test_preprocessors/fixture/input_jmarkdown.md", True),
#     ("tests/test_preprocessors/fixture/input_code.py", False),
#     ("tests/test_preprocessors/fixture/input_not_jmarkdown.md", False),
# ])
# def params(request):
#     with open(request.param[0]) as file:
#         return file.read(), request.param[1]


# def test_remove_input_preprocessor(params):
#     input_str, is_transient = params
#     preprocessor = NbMetadataPreprocessor(jinja=1)

#     cell = MagicMock(name="cell")
#     type(cell).source = PropertyMock(name="source", return_value=input_str)
#     type(cell).cell_type = PropertyMock(name="source", return_value="code")
#     # TODO: not ideal solution
#     type(cell).transient = PropertyMock(name="is_transient", return_value={"remove_source": is_transient})

#     resources = MagicMock(name="resources")
#     index = MagicMock(name="index")

#     cell, resources = preprocessor.preprocess_cell(cell, resources, index)

#     assert cell.transient == {"remove_source": is_transient}


