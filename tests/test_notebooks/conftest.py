import os
from pathlib import Path

import pkg_resources
import pytest
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


@pytest.fixture()
def driver():
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = selenium.webdriver.Chrome(service=chrome_service, options=chrome_options)

    yield driver

    driver.close()


@pytest.fixture
def fixture_dir():
    return "tests/test_notebooks/fixture"


@pytest.fixture
def templates_path():
    return str(Path(pkg_resources.resource_filename("pretty_jupyter", "templates")).as_posix())


@pytest.fixture
def input_path():
    raise NotImplementedError()


@pytest.fixture
def out_path(tmpdir, input_path):
    path = str((Path(tmpdir) / f"{Path(input_path).stem}.html").absolute())

    yield path

    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def page_url(out_path):
    return os.path.normpath(f"file:/{out_path}")
