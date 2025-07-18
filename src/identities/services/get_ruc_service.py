from pydantic import BaseModel
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from core.redis_util import redis_cache


class RucData(BaseModel):
    ruc: str
    business_name: str


def get_ruc_service(ruc: str) -> RucData:
    # Try to get data from cache first
    cached_data = redis_cache.get_data(f"ruc:{ruc}", RucData)
    print(f"cached_data: {cached_data}")
    if cached_data:
        return cached_data

    print("proceed with web scraping")
    # Continue with web scraping if not in cache
    return get_ruc_from_web(ruc)


def get_ruc_from_web(ruc: str) -> RucData:
    driver = createDriver()
    print("Starting")
    try:
        print("Starting scraping web RUC")
        Wait(driver, 10)
        driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias")
        print(f"URL : {driver.current_url}")
        driver.save_screenshot("rucpage.png")
        driver.implicitly_wait(6)
        driver.find_element(By.XPATH, '//*[@id="txtRuc"]').send_keys(ruc)
        driver.find_element(By.ID, "btnAceptar").click()
        business_name_with_ruc = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4"
        ).text
        ruc_data = RucData(
            ruc=ruc,
            business_name=business_name_with_ruc.strip().split(" - ").pop().strip(),
        )
        print(f"ruc:{ruc}", ruc_data)
        redis_cache.save_data(f"ruc:{ruc}", ruc_data)
        return ruc_data
    except NoSuchElementException:
        raise Exception("Business not found")
    except Exception as e:
        print(f"Error: {e}")
        print("Error server")
        raise
    finally:
        driver.quit()
