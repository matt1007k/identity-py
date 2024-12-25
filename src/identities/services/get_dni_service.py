from pydantic import BaseModel
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import NoSuchElementException


class DniData(BaseModel):
    dni: str
    names: str
    paternal_surname: str
    maternal_surname: str


def get_dni_service(dni: str) -> DniData:
    driver = createDriver()
    try:
        wait = Wait(driver, 1)
        driver.get("https://eldni.com")
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

        return DniData(
            dni=dni,
            names=names,
            paternal_surname=paternal_surname,
            maternal_surname=maternal_surname,
        )
    except NoSuchElementException:
        print("Error: El elemento con ID 'dni' no existe.")
        raise
    finally:
        driver.quit()
