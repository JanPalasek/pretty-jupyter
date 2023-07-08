import os
import subprocess
import sys
from pathlib import Path

import nbconvert
import pytest
from packaging import version
from selenium.webdriver.common.by import By


@pytest.fixture
def input_path(fixture_dir):
    path = os.path.join(fixture_dir, "tokens.ipynb")
    return str(Path(path).resolve().as_posix())


def test_tokens(templates_path, input_path, out_path, page_url, driver):
    out_dir = os.path.dirname(out_path)
    python_path = sys.executable
    retval = subprocess.run(
        f'{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs={templates_path} --execute --output-dir="{out_dir}"',
        check=True,
        shell=True,
    )
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    driver.get(page_url)

    main_content = driver.find_element(By.XPATH, "//*[@id = 'main-content']")

    ###########
    # HEADERS #
    ###########
    header = main_content.find_element(By.XPATH, "//div[@id = 'header-id']")
    assert header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Header"
    assert "blue" in header.get_attribute("class")

    header = main_content.find_element(By.XPATH, "//div[@id = 'header-spaces-id']")
    assert header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Header with newlines"
    assert "red" in header.get_attribute("class")

    header = main_content.find_element(By.XPATH, "//div[@id = 'header-whitespaces-id']")
    assert (
        header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Header with whitespaces"
    )
    assert "grey" in header.get_attribute("class")

    ##################
    # MARKDOWN TABLE #
    ##################
    # TODO: nbconvert==7.0.0 has a bug - generating of markdown table doesn't work, issue #1848
    if version.parse(nbconvert.__version__) < version.parse("7.0.0"):
        table = main_content.find_element(By.XPATH, "//table[@id = 'table-id']")
        assert "table-fit" in table.get_attribute("class")

    ################
    # PANDAS TABLE #
    ################
    table = main_content.find_element(By.XPATH, "//table[@id = 'ptable-id']")
    assert "red" in table.get_attribute("class") and "pj-table-ignore" in table.get_attribute(
        "class"
    )

    #################
    # HTML ELEMENTS #
    #################
    paragraph = main_content.find_element(By.XPATH, "//p[@id = 'paragraph-id']")
    assert "white-letter" in paragraph.get_attribute("class") and "red" in paragraph.get_attribute(
        "class"
    )
