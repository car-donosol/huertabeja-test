import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime

BASE_URL = "https://huertabejafs.vercel.app"


def register(driver, nombre, email, password, confirmpass):
    """Realiza el registro y detecta mensaje dinámico de éxito o error."""
    driver.get(f"{BASE_URL}/account/register")

    # Esperar carga del formulario
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))

    # Llenar campos
    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "name").send_keys(nombre)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").clear()
    driver.find_element(By.ID, "confirmPassword").send_keys(confirmpass)

    # Aceptar términos y condiciones
    try:
        checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'][required]"))
        )
        driver.execute_script("arguments[0].click();", checkbox)
    except Exception:
        print("No se encontró el checkbox de términos y condiciones.")

    # Enviar formulario
    try:
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn)
    except Exception:
        print("No se encontró el botón de registro.")

    # Esperar mensaje (éxito o error)
    try:
        msg_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'p-4') and contains(@class,'font-medium')]")
            )
        )
        message_text = msg_el.text.strip()
        if "exitoso" in message_text.lower():
            print(f"Registro exitoso para {email}: {message_text}")
            return "exitoso"
        else:
            print(f"Error al registrar {email}: {message_text}")
            return message_text
    except Exception:
        print(f"No se detectó ningún mensaje para {email}")
        return "sin mensaje"


def main():
    df = pd.read_csv("data.csv")

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")  # Descomentar para modo sin ventana
    service = Service(ChromeDriverManager().install())

    print("\nIniciando registro de usuarios...\n")

    for i, row in df.head(3).iterrows():  # Solo los 3 primeros
        nombre = row["nombre"]
        email = row["email"]
        password = row["password"]
        confirmpass = row["confirmpass"]

        print(f"Registrando usuario {i+1}/3: {nombre} ({email})")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(5)

        try:
            estado = register(driver, nombre, email, password, confirmpass)
        except Exception as e:
            print(f"Error inesperado con {email}: {e}")
        finally:
            driver.quit()
            time.sleep(2)

    print("\nRegistro finalizado correctamente.")


if __name__ == "__main__":
    main()
