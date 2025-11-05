import time
import random
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


def login(driver, email, password):
    """Inicia sesión en Huertabeja y devuelve estado."""
    driver.get(f"{BASE_URL}/account/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    try:
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    except Exception:
        print("No se encontró el botón de inicio de sesión.")

    try:
        msg_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'p-4') and contains(@class,'font-medium')]"))
        )
        text = msg_el.text.strip()
        if "exitoso" in text.lower():
            print(f"Login exitoso: {email}")
            return "exitoso"
        else:
            print(f"Error al iniciar sesión ({email}): {text}")
            return text
    except Exception:
        print(f"No se detectó mensaje para {email}")
        return "sin mensaje"


def register_new_user(driver):
    """Registra un nuevo usuario aleatorio (acepta términos automáticamente)."""
    driver.get(f"{BASE_URL}/account/register")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))

    nombres = ["valentina", "sebastian", "camila", "ignacio", "sofia"]
    dominios = ["@gmail.com", "@duocuc.cl"]

    nombre = random.choice(nombres)
    email = f"{nombre}{random.randint(100,999)}{random.choice(dominios)}"
    password = "123456"

    # Llenar campos
    driver.find_element(By.ID, "name").send_keys(nombre)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").send_keys(password)

    # Aceptar los términos y condiciones
    try:
        checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'][required]"))
        )
        driver.execute_script("arguments[0].click();", checkbox)
        if checkbox.is_selected():
            print("Términos y condiciones aceptados correctamente.")
        else:
            print("El checkbox no quedó seleccionado.")
    except Exception:
        print("No se pudo hacer clic en el checkbox de términos y condiciones.")

    # Enviar formulario
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Esperar mensaje de resultado
    try:
        msg_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'p-4') and contains(@class,'font-medium')]"))
        )
        text = msg_el.text.strip()
        print(f"{text} → {email}")
    except:
        print("No se detectó mensaje de registro.")

    return email, password


def main():
    df = pd.read_csv("data.csv")

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")  # Activa si no quieres ver el navegador
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    resultados = []
    print("\nIniciando test de inicio de sesión...\n")

    # 1. Intentar 2 inicios de sesión erróneos
    for i, row in df.head(2).iterrows():
        email, password = row["email"], row["password"]
        print(f"Intentando login con usuario inválido: {email}")
        estado = login(driver, email, "clave_incorrecta")
        resultados.append({"email": email, "resultado": estado})
        time.sleep(1.5)

    # 2. Registrar nuevo usuario
    print("\nRegistrando nuevo usuario...\n")
    email, password = register_new_user(driver)
    time.sleep(2)

    # 3. Iniciar sesión con el nuevo usuario
    print("\nIniciando sesión con usuario recién registrado...\n")
    estado = login(driver, email, password)
    resultados.append({"email": email, "resultado": estado})

    # 4. Resultados finales
    print("\nResultados del test:")
    for r in resultados:
        print(f" - {r['email']}: {r['resultado']}")

    print("\nTest de login finalizado correctamente.")
    driver.quit()


if __name__ == "__main__":
    main()
