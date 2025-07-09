from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from requests.exceptions import ConnectionError


def createDriver() -> webdriver.Chrome:
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("--no-sandbox")
        option.add_argument("--headless")
        option.add_argument("--window-size=1920,1080")
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option("useAutomationExtension", False)
        print("driver created")

        service = Service(ChromeDriverManager().install())
        driver = Chrome(service=service, options=option)
        return driver
    except ConnectionError:
        raise ConnectionError(
            "No internet connection available. Please check your network connection."
        )
    except Exception as e:
        raise Exception(f"Failed to create web driver: {str(e)}")
