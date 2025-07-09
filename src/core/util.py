from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from requests.exceptions import ConnectionError


def createDriver() -> webdriver.Chrome:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        print("driver created")

        service = Service(ChromeDriverManager().install())
        driver = Chrome(service=service, options=options)
        return driver
    except ConnectionError:
        raise ConnectionError(
            "No internet connection available. Please check your network connection."
        )
    except Exception as e:
        raise Exception(f"Failed to create web driver: {str(e)}")
