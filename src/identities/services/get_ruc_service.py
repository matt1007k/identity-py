from pydantic import BaseModel
from core.util import createDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class RucData(BaseModel):
    ruc: str
    business_name: str


def get_ruc_service(ruc: str) -> RucData:
    driver = createDriver()
    try:
        driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias")
        driver.implicitly_wait(6)
        driver.find_element(By.XPATH, '//*[@id="txtRuc"]').send_keys(ruc)
        driver.find_element(By.ID, "btnAceptar").click()
        business_name_with_ruc = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]/h4"
        ).text
        return RucData(
            ruc=ruc,
            business_name=business_name_with_ruc.strip().split("-").pop(),
        )
    except NoSuchElementException:
        raise Exception("Business not found")
    except:
        raise
    finally:
        driver.quit()
