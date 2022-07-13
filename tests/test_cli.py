from click.testing import CliRunner
import pytest
from pretty_jupyter.console import cli
import os
from selenium.webdriver.common.by import By

@pytest.fixture
def input_path():
    return "tests/fixture/notebook.ipynb"


def test_nbconvert(input_path, tmpdir, driver):
    out_path = os.path.normpath(os.path.join(tmpdir, "actual.html"))

    runner = CliRunner()
    result = runner.invoke(cli, ["nbconvert", input_path, "--out", out_path])
    
    assert result.exit_code == 0

    assert os.path.exists(out_path), "The expected file does not exist."

    # go to page
    driver.get(os.path.abspath(out_path))

    # check the title
    title_xpath = "//h1[@class='title']"
    assert driver.find_element(By.XPATH, title_xpath).text == "Notebook"

    # test whether there is expected number of headers of level 1
    h1_xpath = "//div[contains(@class, 'level1') and contains(@class, 'section')]/h1"
    assert len(driver.find_elements(By.XPATH, h1_xpath)) == 4

    # check the tabset more in-depth
    assert driver.find_elements(By.XPATH, h1_xpath)[2].text == "Chapter 1: Tabs"

    tab_section = driver.find_elements(By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]")[2]

    # select tabs
    list_tabs = tab_section.find_elements(By.XPATH, "ul[contains(@class, 'nav') and contains(@class, 'nav-pills')]/li")

    assert len(list_tabs) == 3, "There should be 3 tabs."
    assert list_tabs[1].text == "Tab 2", "The name of the second tab should be 'Tab 2'."


    tab_contents = tab_section.find_elements(By.XPATH, """div[contains(@class, 'tab-content')]
        /div[contains(@class, 'section') and contains(@class, 'level2') and contains(@class, 'tab-pane')]""")
    assert len(tab_contents) == 3, "There should be 3 tab contents for the tabs."

    assert "active" in tab_contents[0].get_attribute("class"), "First tab should be active at the beginning."

    # click on the second tab
    list_tabs[1].click()

    assert "active" in tab_contents[1].get_attribute("class"), "Second tab should be active after clicking on it."

    # check that the maths rendered properly
    assert len(tab_contents[1].find_elements(By.XPATH, "span[contains(@class, 'MJXc-display')]")) > 0, "Math didn't render."

    # check that the maths rendered properly
    math_text = tab_contents[1].find_element(By.XPATH, "script[contains(@type, 'math/tex')]").get_attribute("innerHTML")
    assert math_text == r"a \cdot a^2 = \frac{a^5}{a^2} = a^3 = 125"
    
    # code folding
    jmd_section = driver.find_elements(By.XPATH, "//div[contains(@class, 'section') and contains(@class, 'level1')]")[3]

    code_div = jmd_section.find_elements(By.XPATH, "div[contains(@class, 'py-code-collapse') and contains(@class, 'collapse')]")[0]
    assert len(code_div.find_elements(By.XPATH, "div[contains(@class, 'pj-input')]//pre/span")) > 0, "Code highlighting does not work."

    # table of contents
    def get_y_location(driver):
        scroll_position_script = """
                var pageY;
                if (typeof(window.pageYOffset) == 'number') {
                    pageY = window.pageYOffset;
                } else {
                    pageY = document.documentElement.scrollTop;
                }
                return pageY;
            """

        return driver.execute_script(scroll_position_script)

    toc = driver.find_elements(By.XPATH, "//div[@id='TOC']")[0]

    toc_first_level = toc.find_elements(By.XPATH, "ul")
    assert len(toc_first_level) == 3, "There are 3 chapters."

    # click on the Chapter 2: Jinja Markdown
    toc_first_level[2].find_element(By.XPATH, "li").click()
    import time
    time.sleep(2)

    jmd_title = jmd_section.find_element(By.XPATH, "h1")
    tab_section_title = tab_section.find_element(By.XPATH, "h1")

    epsilon_px = 10
    assert abs(jmd_title.location["y"] - get_y_location(driver)) < epsilon_px, "Chapter 2: Jinja Markdown must be visible after clicking on it in TOC."
    assert tab_section_title.location["y"] < get_y_location(driver), "Chapter 1: Tabs cannot be visible after clicking on chapter 2."

    # go to Chapter 1
    toc_first_level[1].find_element(By.XPATH, "li").click()
    time.sleep(2)
    assert abs(tab_section_title.location["y"] - get_y_location(driver)) < epsilon_px, "Chapter 1: Tabs must be visible after clicking on chapter 1."