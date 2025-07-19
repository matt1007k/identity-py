from pydantic import BaseModel
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import NoSuchElementException
from core.redis_util import redis_cache

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DniData(BaseModel):
    dni: str
    names: str
    paternal_surname: str
    maternal_surname: str
    verification_code: str

    @classmethod
    def from_text(cls, text: str):
        parsed_data = {}
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if "Número de DNI" in key:
                    parsed_data["dni"] = value
                elif "Nombres" in key:
                    parsed_data["names"] = value
                elif "Apellido Paterno" in key:
                    parsed_data["paternal_surname"] = value
                elif "Apellido Materno" in key:
                    parsed_data["maternal_surname"] = value
                elif "Código de Verificación" in key:
                    parsed_data["verification_code"] = value

        # Pydantic automáticamente validará los datos al crear la instancia
        return cls(**parsed_data)


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def get_dni_service(dni: str) -> DniData:
    # Try to get data from cache first
    cached_data = redis_cache.get_data(f"dni:{dni}", DniData)
    print(f"cached_data: {cached_data}")
    if cached_data:
        return cached_data

    print("proceed with web scraping")
    # If not in cache, proceed with web scraping
    return get_dni_from_web(dni)


def get_dni_from_web(dni: str) -> DniData:
    # driver = createDriver()
    print("Starting")
    try:
        print("Starting scraping web DNI")
        wait = Wait(driver, 10)
        driver.get("https://dniperu.com/buscar-dni-nombres-apellidos")
        print(driver.title)
        print(f"URL : {driver.current_url}")
        driver.save_screenshot("dnipage.png")
        driver.find_element(By.ID, "dni4").send_keys(dni)
        driver.find_element(By.ID, "buscar-dni-button").click()

        result_container = wait.until(
            EC.presence_of_element_located((By.ID, "resultado_dni"))
        ).get_attribute("value")

        print(f"result {result_container}")

        dni_data = DniData.from_text(result_container or "")
        print(f"dni:{dni}", dni_data)

        # Save to cache before returning
        redis_cache.save_data(f"dni:{dni}", dni_data)
        return dni_data

    except NoSuchElementException as e:
        print(f"Error: {e}")
        print("Error: El elemento html no se encontró")
        raise
    except Exception as e:
        print(f"Error: {e}")
        print("Error server")
        raise
    finally:
        driver.quit()
