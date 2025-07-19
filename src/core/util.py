from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchDriverException, SessionNotCreatedException
from requests.exceptions import ConnectionError


def createDriver() -> webdriver.Chrome:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        print("service created")
        driver = Chrome(service=service, options=options)
        print("driver created")

        print(f"Driver: {driver.title}")
        return driver
    except ConnectionError:
        raise ConnectionError(
            "No internet connection available. Please check your network connection."
        )
    except NoSuchDriverException as e:
        raise Exception(f"Failed no found web driver: {str(e)}")
    except SessionNotCreatedException as e:
        raise Exception(f"Failed session not created: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to create web driver: {str(e)}")
