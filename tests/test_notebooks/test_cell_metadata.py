import os
import subprocess
import sys
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By


@pytest.fixture
def input_path(fixture_dir):
    path = os.path.join(fixture_dir, "cell_metadata.ipynb")
    return str(Path(path).resolve().as_posix())


def test_cell_metadata(templates_path, input_path, out_path, page_url, driver):
    out_dir = os.path.dirname(out_path)
    python_path = sys.executable
    retval = subprocess.run(
        f'{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs={templates_path} --execute --ExecutePreprocessor.allow_errors=True --output-dir="{out_dir}"',
        check=True,
        shell=True,
    )
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    driver.get(page_url)

    main_content = driver.find_element(By.XPATH, "//*[@id = 'main-content']")

    code_folding_inputs = main_content.find_elements(
        By.XPATH, "//*[contains(@class, 'py-code-collapse')]"
    )
    assert len(code_folding_inputs) == 4, "There must be 4 code folding input cells."

    assert "input: true, input_fold: show" in code_folding_inputs[0].get_attribute(
        "innerHTML"
    ), "First jinja markdown cell should have input: true and input_fold: show."
    jmd_button = code_folding_inputs[0].find_element(
        By.XPATH, "preceding-sibling::div[@class = 'row'][1]//button/span"
    )
    assert jmd_button.get_attribute("innerHTML") == "Hide", "The first jmd button should be shown."

    error_output = main_content.find_elements(By.XPATH, "//pre[contains(@class, 'bg-danger')]")
    assert (
        len(error_output) == 1
    ), "The generated page should have one error output right in the end."
