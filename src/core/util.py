from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from requests.exceptions import ConnectionError

from core.config.env import BROWSER_URL


def createDriver() -> webdriver.Chrome:
    try:
        # option = webdriver.ChromeOptions()
        option = webdriver.FirefoxOptions()
        option.add_argument("--no-sandbox")
        # option.add_argument("--headless")
        option.add_argument("--window-size=1920,1080")
        print("driver created")
        driver = webdriver.Remote(
            command_executor=BROWSER_URL,
            options=option,
        )
        print(f"driver {driver}")
        # service = Service(ChromeDriverManager().install())
        # driver = Chrome(service=service, options=option)
        return driver
    except ConnectionError:
        raise ConnectionError(
            "No internet connection available. Please check your network connection."
        )
    except Exception as e:
        raise Exception(f"Failed to create web driver: {str(e)}")
