import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By


@pytest.fixture
def input_path(fixture_dir):
    path = os.path.join(fixture_dir, "lang.ipynb")
    return str(Path(path).resolve().as_posix())


def test_lang(templates_path, input_path, out_path, page_url, driver):
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

    # CZECH
    header = main_content.find_element(By.XPATH, "//div[@id = 'Čeština']")
    assert header.find_element(By.XPATH, "h1").get_attribute("innerHTML") == "Čeština"

    header = main_content.find_element(By.XPATH, "//div[@id = 'Hlavička-s-českými-znaky-O_O-1']")
    assert (
        header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Hlavička s českými znaky"
    )

    header = main_content.find_element(By.XPATH, "//div[@id = 'Hlavička-s-českými-znaky-O_O-2']")
    assert (
        header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Hlavička s českými znaky"
    )

    # note: 23 is encoded hash character
    tab = main_content.find_element(
        By.XPATH, "//a[@href = '#Český-Tab-s-divnými-znaky--_23-O_O-2']/.."
    )
    tab_sec = main_content.find_element(
        By.XPATH, "//div[@id = 'Český-Tab-s-divnými-znaky--_23-O_O-2']"
    )
    assert "active" not in main_content.get_attribute("class")
    tab.click()
    time.sleep(0.5)
    assert "active" in tab_sec.get_attribute("class")

    header = main_content.find_element(By.XPATH, "//div[@id = 'české-id']")
    assert (
        header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Unikátní česká hlavička"
    )

    # RUSSIAN
    header = main_content.find_element(By.XPATH, "//div[@id = 'ру́сский-язы́к']")
    assert header.find_element(By.XPATH, "h1").get_attribute("innerHTML") == "ру́сский язы́к"

    header = main_content.find_element(By.XPATH, "//div[@id = 'Бланк-с-буквами-O_O-1']")
    assert header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Бланк с буквами"

    header = main_content.find_element(By.XPATH, "//div[@id = 'Бланк-с-буквами-O_O-2']")
    assert header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Бланк с буквами"

    tab = main_content.find_element(By.XPATH, "//a[@href = '#вкладка-O_O-2']/..")
    tab_sec = main_content.find_element(By.XPATH, "//div[@id = 'вкладка-O_O-2']")
    assert "active" not in main_content.get_attribute("class")
    tab.click()
    time.sleep(0.5)
    assert "active" in tab_sec.get_attribute("class")

    header = main_content.find_element(By.XPATH, "//div[@id = 'Российский-ID']")
    assert header.find_element(By.XPATH, "h2").get_attribute("innerHTML") == "Уникальный заголовок"
