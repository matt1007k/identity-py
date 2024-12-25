from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def createDriver() -> webdriver.Chrome:
    # option = webdriver.ChromeOptions()
    option = webdriver.FirefoxOptions()
    option.add_argument("--no-sandbox")
    option.add_argument("--headless")
    option.add_argument("--window-size=1920,1080")
    driver = webdriver.Remote(
        command_executor="http://0.0.0.0:4444",
        options=option,
    )
    # service = Service(ChromeDriverManager().install())
    # driver = Chrome(service=service, options=option)
    return driver
