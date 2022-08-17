from click.testing import CliRunner
import pytest
from pretty_jupyter.console import cli
import os
from selenium.webdriver.common.by import By
from pathlib import Path
import sys
import subprocess
import pkg_resources


@pytest.fixture
def input_path(fixture_dir):
    return os.path.join(fixture_dir, "toc.ipynb")

@pytest.fixture
def out_dir(tmpdir):
    return tmpdir

@pytest.fixture
def out_path(input_path):
    return str((Path(out_dir) / f"{Path(input_path).stem}.html").absolute())


def test_toc(input_path, out_dir, out_path, driver):
    templates_path = str(Path(pkg_resources.resource_filename("pretty_jupyter", "templates")).as_posix())
    input_path = str(Path(input_path).resolve().as_posix())

    python_path = sys.executable
    retval = subprocess.run(f"{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs {templates_path} --execute --output-dir {out_dir}", check=True, shell=True)
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    
    out_path = str((Path(out_dir) / f"{Path(input_path).stem}.html").absolute())
    url = os.path.normpath(f"file:/{out_path}")
    # # go to page
    driver.get(url)

    # # check the title
    # title_xpath = "//h1[@class='title']"
    # assert driver.find_element(By.XPATH, title_xpath).text == "Test Notebook"

    # main_content = driver.find_element(By.XPATH, "//*[@id = 'main-content']")
    print(url)