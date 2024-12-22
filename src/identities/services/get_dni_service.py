from pydantic import BaseModel
from src.core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait


class DniResponse(BaseModel):
    dni: str
    names: str
    paternal_surname: str
    maternal_surname: str


def get_dni_service(dni: str) -> DniResponse:
    print(dni)
    driver = createDriver()
    driver.get("https://eldni.com")
    driver.find_element(By.ID, "dni").send_keys(dni)
    driver.find_element(By.ID, "btn-buscar-datos-por-dni").click()
    names = driver.find_element(By.ID, "nombres").get_attribute("value")
    paternal_surname = driver.find_element(By.ID, "apellidop").get_attribute("value")
    maternal_surname = driver.find_element(By.ID, "apellidom").get_attribute("value")
    print(f"names {names}")
    print(f"paternal_surname {paternal_surname}")
    print(f"maternal_surname {maternal_surname}")
    return DniResponse(
        dni=dni,
        names=names,
        paternal_surname=paternal_surname,
        maternal_surname=maternal_surname,
    )
