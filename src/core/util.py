from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def createDriver() -> webdriver.Chrome:
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--window-size=1920,1080")
    return Chrome(service=service, options=option)
