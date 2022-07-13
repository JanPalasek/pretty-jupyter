import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import selenium.webdriver


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
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = selenium.webdriver.Chrome(service=chrome_service, options=chrome_options)

    yield driver

    driver.close()