import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://huertabejafs.vercel.app"

def obtener_botones(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[.//button[contains(., 'Ver producto')]]"))
    )
    return driver.find_elements(By.XPATH, "//a[.//button[contains(., 'Ver producto')]]")

def agregar_producto(driver, indice, contador):
    try:
        botones = obtener_botones(driver)
        boton = botones[indice]
        driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", boton)
        time.sleep(random.uniform(0.6, 1.2))
        boton.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Agregar al carrito')]"))
        )

        nombre = driver.find_element(By.TAG_NAME, "h1").text if driver.find_elements(By.TAG_NAME, "h1") else f"Producto {indice+1}"

        driver.find_element(By.XPATH, "//button[contains(., 'Agregar al carrito')]").click()
        time.sleep(random.uniform(0.8, 1.6))

        print(f"'{nombre}' agregado correctamente al carrito ({contador} items)")
        driver.get(BASE_URL)

    except Exception as e:
        print(f"Error con producto #{indice + 1}: {e}")
        driver.get(BASE_URL)

def checkout(driver):
    driver.get(f"{BASE_URL}/checkout")
    try:
        driver.find_element(By.XPATH, "//h2[contains(., 'Tu carrito está vacío')]")
        print("Carrito vacío")
        return
    except:
        pass

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstName")))

        campos = {
            "firstName": "Valentina",
            "lastName": "Rojas",
            "email": "valentina.rojas@gmail.com",
            "phone": "987654321",
            "address": "Av. Las Flores 123",
            "city": "Santiago",
            "postalCode": "8320000",
            "cardNumber": "4111 1111 1111 1111",
            "cardName": "VALENTINA ROJAS",
            "expiryDate": "12/29",
            "cvv": "123"
        }

        for k, v in campos.items():
            try:
                driver.find_element(By.ID, k).send_keys(v)
            except:
                pass

        try:
            region = driver.find_element(By.ID, "region")
            region.find_element(By.XPATH, ".//option[@value='metropolitana']").click()
        except:
            pass

        driver.find_element(By.XPATH, "//button[contains(., 'Pagar')]").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(., '¡Pedido confirmado!')]"))
        )
        print("Pedido confirmado exitosamente")

    except:
        print("No se detectó mensaje de confirmación")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    print("Iniciando compra...")

    botones = obtener_botones(driver)
    total_disponibles = len(botones)

    # Selecciona entre 3 y 6 productos al azar
    cantidad = random.randint(3, 6)
    indices = random.sample(range(total_disponibles), cantidad)

    for i, idx in enumerate(indices, start=1):
        agregar_producto(driver, idx, i)
        time.sleep(random.uniform(1.0, 2.0))

    print("\nRealizando checkout...")
    checkout(driver)

    driver.quit()

if __name__ == "__main__":
    main()
