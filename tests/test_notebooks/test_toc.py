import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By

from pretty_jupyter.constants import TOKEN_SEP
from pretty_jupyter.testing import is_visible


@pytest.fixture
def input_path(fixture_dir):
    path = os.path.join(fixture_dir, "toc.ipynb")
    return str(Path(path).resolve().as_posix())


def test_toc(templates_path, input_path, out_path, page_url, driver):
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

    toc = driver.find_elements(By.XPATH, "//div[@id='TOC']")[0]

    # check that there are two chapter
    toc_first_level = toc.find_elements(By.XPATH, "ul")
    assert len(toc_first_level) == 2, "There are 2 chapters."

    # check that first section is visible
    toc_first_level[0].find_element(By.XPATH, "li").click()
    time.sleep(2)
    first_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]"
    )[0]
    first_header = first_chapter.find_element(By.XPATH, "h1")
    assert is_visible(
        element=first_header, driver=driver
    ), "First chapter should be visible at the beginning."

    # go to second chapter and check that it is visible and the first section is not (should be scrolled away)
    toc_first_level[1].find_element(By.XPATH, "li").click()
    time.sleep(2)
    toc_first_level[1].find_element(By.XPATH, "li").click()
    time.sleep(2)
    second_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]"
    )[1]
    second_header = second_chapter.find_element(By.XPATH, "h1")
    assert is_visible(
        element=second_header, driver=driver
    ), "Second chapter should be visible after scrolling to it."
    assert not is_visible(
        element=first_header, driver=driver
    ), "First chapter shouldn't be visible because we scrolled to the second one."


# YAML config is one-line because windows cmd probably doesn't support multiline
NOT_GENERATED_METADATA = "{ output: { html: { toc: false } } }"


def test_toc_not_generated(templates_path, input_path, out_path, page_url, driver):
    out_dir = os.path.dirname(out_path)
    python_path = sys.executable
    retval = subprocess.run(
        f'{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs="{templates_path}" --execute --output-dir="{out_dir}" --HtmlNbMetadataPreprocessor.pj_metadata="{NOT_GENERATED_METADATA}"',
        check=True,
        shell=True,
    )
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    driver.get(page_url)

    toc = driver.find_elements(By.XPATH, "//div[@id='TOC']")
    assert len(toc) == 0, "TOC shouldnt've been generated"


NUMBER_SECTIONS_METADATA = "{ output: { html: { number_sections: true }} }"


def test_toc_number_sections(templates_path, input_path, out_path, page_url, driver):
    out_dir = os.path.dirname(out_path)
    python_path = sys.executable
    retval = subprocess.run(
        f'{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs="{templates_path}" --execute --output-dir="{out_dir}" --HtmlNbMetadataPreprocessor.pj_metadata="{NUMBER_SECTIONS_METADATA}"',
        check=True,
        shell=True,
    )
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    driver.get(page_url)

    main_content = driver.find_element(By.XPATH, "//*[@id = 'main-content']")

    second_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]/h1"
    )[1]
    assert second_chapter.get_attribute("innerHTML") == "2. Level 1"

    third_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]/h1"
    )[2]
    assert (
        third_chapter.get_attribute("innerHTML") == "Level 1"
    ), "The third Level 1 has been marked as unnumbered."

    # test that Level 3s are numbered and they follow the proper naming convention
    assert (
        main_content.find_element(By.XPATH, f"//*[@id = 'Level-2-O_O-1']/h2").get_attribute(
            "innerHTML"
        )
        == "1.1. Level 2"
    )
    assert (
        main_content.find_element(By.XPATH, f"//*[@id = 'Level-2-O_O-2']/h2").get_attribute(
            "innerHTML"
        )
        == "2.1. Level 2"
    )
