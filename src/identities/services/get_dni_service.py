from pydantic import BaseModel
from core.config.env import REDIS_HOST, REDIS_PORT
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import NoSuchElementException
from core.redis_util import redis_cache


class DniData(BaseModel):
    dni: str
    names: str
    paternal_surname: str
    maternal_surname: str


def get_dni_service(dni: str) -> DniData:
    # Try to get data from cache first
    cached_data = redis_cache.get_data(f"dni:{dni}", DniData)
    print(f"cached_data: {cached_data}")
    if cached_data:
        return cached_data

    print("pass")
    # If not in cache, proceed with web scraping
    return get_dni_from_web(dni)


def get_dni_from_web(dni: str) -> DniData:
    driver = createDriver()
    try:
        wait = Wait(driver, 1)
        driver.get("https://eldni.com")
        driver.save_screenshot("dnipage.png")
        driver.find_element(By.ID, "dni").send_keys(dni)
        driver.find_element(By.ID, "btn-buscar-datos-por-dni").click()

        names = wait.until(
            EC.presence_of_element_located((By.ID, "nombres"))
        ).get_attribute("value")
        paternal_surname = wait.until(
            EC.presence_of_element_located((By.ID, "apellidop"))
        ).get_attribute("value")
        maternal_surname = wait.until(
            EC.presence_of_element_located((By.ID, "apellidom"))
        ).get_attribute("value")

        dni_data = DniData(
            dni=dni,
            names=names,
            paternal_surname=paternal_surname,
            maternal_surname=maternal_surname,
        )

        # Save to cache before returning
        redis_cache.save_data(f"dni:{dni}", dni_data)
        return dni_data

    except NoSuchElementException:
        print("Error: El elemento con ID 'dni' no existe.")
        raise
    # except Exception :
    #     print(f"Error: {e}")
    #     print("Error server")
    #     raise
    finally:
        driver.quit()
