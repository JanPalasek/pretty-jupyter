import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By

from pretty_jupyter.testing import is_visible


@pytest.fixture
def input_path(fixture_dir):
    path = os.path.join(fixture_dir, "tabset.ipynb")
    return str(Path(path).resolve().as_posix())


def test_tabset(templates_path, input_path, out_path, page_url, driver):
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

    ################
    # BASIC TABSET #
    ################
    first_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]"
    )[0]

    list_tabs = first_chapter.find_elements(
        By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li"
    )
    tab_contents = first_chapter.find_elements(
        By.XPATH,
        """div[contains(@class, 'tab-content')]
        /div[contains(@class, 'section') and contains(@class, 'level2') and contains(@class, 'tab-pane')]""",
    )

    assert len(list_tabs) == 2, "There should be 2 tabs."
    assert list_tabs[1].text == "Tab 2", "The name of the second tab should be 'Tab 2'."
    assert "active" in list_tabs[1].get_attribute("class"), "Tab 2 should be active."
    assert len(tab_contents) == 2, "There should be 2 tab contents for the tabs."
    assert not tab_contents[0].is_displayed(), "Tab 1 shouldn't be displayed right now."
    assert tab_contents[1].is_displayed(), "Tab 2 should be displayed right now."

    # click on the first tab
    list_tabs[0].click()
    time.sleep(0.5)
    assert "active" in list_tabs[0].get_attribute("class") and "active" not in list_tabs[
        1
    ].get_attribute("class"), "Now tab 2 should be active"
    assert tab_contents[0].is_displayed(), "Tab 1 should be displayed right now."
    assert not tab_contents[1].is_displayed(), "Tab 2 shouldn't be displayed right now."

    #################
    # NESTED TABSET #
    #################
    second_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]"
    )[1]

    tab1_list = second_chapter.find_elements(
        By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li"
    )
    tab1_contents = second_chapter.find_elements(
        By.XPATH,
        """div[contains(@class, 'tab-content')]
        /div[contains(@class, 'section') and contains(@class, 'level2') and contains(@class, 'tab-pane')]""",
    )

    assert len(tab1_list) == 2, "The first level of nested tabset has two options."
    assert tab1_contents[0].is_displayed(), "First tab on the second level is currently shown."
    assert not tab1_contents[
        1
    ].is_displayed(), "Second tab on the first level is currently not shown."

    tab1_list[1].click()
    time.sleep(0.5)
    assert tab1_contents[1].is_displayed(), "Second tab should be shown."

    tab2_list = tab1_contents[1].find_elements(
        By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li"
    )
    tab2_contents = tab1_contents[1].find_elements(
        By.XPATH,
        """div[contains(@class, 'tab-content')]
        /div[contains(@class, 'section') and contains(@class, 'level3') and contains(@class, 'tab-pane')]""",
    )
    assert len(tab2_contents) == 3 and len(tab2_list) == 3
    assert tab2_contents[2].is_displayed(), "Tab 23 should be displayed initially."

    tab2_list[0].click()
    time.sleep(0.5)
    assert tab2_contents[0].is_displayed(), "Tab 21 should be displayed now."

    ################
    # CONTINUATION #
    ################
    third_chapter = main_content.find_elements(
        By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]"
    )[2]

    # two tabsets are there with an invisible title
    # the third is section after the tabset
    tabsets = third_chapter.find_elements(
        By.XPATH, "div[contains(@class, 'section') and contains(@class, 'level2')]"
    )
    continuation1 = third_chapter.find_element(By.XPATH, "//span[@id='continuation1']")
    continuation2 = third_chapter.find_element(By.XPATH, "//span[@id='continuation2']")

    assert (
        len(tabsets) == 3
    ), "There should be 3 sections, where the first two are tabsets and the last is section after it."
    tabset1 = tabsets[0]
    list_tabs = tabset1.find_elements(
        By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li"
    )
    tab_contents = tabset1.find_elements(
        By.XPATH,
        """div[contains(@class, 'tab-content')]
        /div[contains(@class, 'section') and contains(@class, 'level3') and contains(@class, 'tab-pane')]""",
    )
    assert tab_contents[0].is_displayed(), "Tab 1 should be displayed at the beginning."
    assert not tab_contents[1].is_displayed(), "Tab 2 should not be displayed at the beginning."
    assert continuation1.is_displayed(), "Text between should be visible all the time."
    assert continuation2.is_displayed(), "Text in the end should be visible all the time."

    list_tabs[1].click()
    time.sleep(0.5)
    assert not tab_contents[0].is_displayed(), "Tab 1 should not be displayed."
    assert tab_contents[1].is_displayed(), "Tab 2 should be displayed."
    assert continuation1.is_displayed(), "Text between should be visible all the time."
    assert continuation2.is_displayed(), "Text in the end should be visible all the time."


NO_TABSET_METADATA = "{ output: { html: { tabset: false }} }"


def test_no_tabset(templates_path, input_path, out_path, page_url, driver):
    out_dir = os.path.dirname(out_path)
    python_path = sys.executable
    retval = subprocess.run(
        f'{python_path} -m jupyter nbconvert --to html --template pj {input_path} --TemplateExporter.extra_template_basedirs={templates_path} --execute --output-dir="{out_dir}" --HtmlNbMetadataPreprocessor.pj_metadata="{NO_TABSET_METADATA}"',
        check=True,
        shell=True,
    )
    assert retval.returncode == 0, "jupyter nbconvert command ended up with a failure"
    driver.get(page_url)

    all_tabs = driver.find_elements(
        By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li"
    )

    assert len(all_tabs) == 0, "Tabset is turned off but the tabs have been generated."
