from pydantic import BaseModel
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from core.redis_util import redis_cache


class RucData(BaseModel):
    ruc: str
    business_name: str


def get_ruc_service(ruc: str) -> RucData:
    # Try to get data from cache first
    cached_data = redis_cache.get_data(f"ruc:{ruc}", RucData)
    if cached_data:
        return cached_data

    # Continue with web scraping if not in cache
    return get_ruc_from_web(ruc)


def get_ruc_from_web(ruc: str) -> RucData:
    driver = createDriver()

    try:
        driver.get_network_conditions()
        driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias")
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
        redis_cache.save_data(f"ruc:{ruc}", ruc_data)
        return ruc_data
    except NoSuchElementException:
        raise Exception("Business not found")
    except:
        raise
    finally:
        driver.quit()
