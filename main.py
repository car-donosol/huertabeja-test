import subprocess
import time
import sys
from pathlib import Path

# Rutas a los scripts (ajusta si están en carpetas distintas)
ROOT = Path(__file__).parent
REGISTER = ROOT / "register.py"
LOGIN = ROOT / "login.py"
COMPRA = ROOT / "compra.py"

def run_script(path, name):
    print(f"\nEjecutando {name}...\n")
    try:
        result = subprocess.run([sys.executable, str(path)], check=True)
        print(f"{name} finalizado correctamente.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {name} (código {e.returncode}).\n")
        sys.exit(1)

def main():
    print("==== TESTING HUERTABEJA ====\n")

    # 1. Registro
    run_script(REGISTER, "Registro")

    # Espera breve antes de iniciar sesión
    time.sleep(2)

    # 2. Login
    run_script(LOGIN, "Inicio de sesión")

    # Espera breve antes de la compra
    time.sleep(2)

    # 3. Compra
    run_script(COMPRA, "Compra")

    print("\nFlujo completo finalizado exitosamente.")

if __name__ == "__main__":
    main()
