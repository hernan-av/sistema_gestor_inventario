# Módulo de configuración y manejo de logs
# Este módulo se encarga de configurar el registro de logs, 
# creando una carpeta para los archivos de logs y definiendo 
# funciones para registrar mensajes de nivel INFO y ERROR.

import logging
import os
from datetime import datetime

# Crear carpeta de logs si no existe
LOG_DIR = "."
os.makedirs(LOG_DIR, exist_ok=True)

# Formato del archivo según fecha
fecha_actual = datetime.now().strftime("%Y-%m-%d")
LOG_PATH = os.path.join(LOG_DIR, f"log_{fecha_actual}.log")

# Configuración básica para el logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] → %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),  # Guardar log en archivo
        # logging.StreamHandler()  # Descomentar si se desea imprimir en consola
    ]
)

def log_info(mensaje: str):
    """
    Registra un mensaje de nivel INFO en el archivo de logs.

    Parámetros:
        mensaje (str): El mensaje que se registrará en el log.
    """
    logging.info(mensaje)

def log_error(mensaje: str):
    """
    Registra un mensaje de nivel ERROR en el archivo de logs.

    Parámetros:
        mensaje (str): El mensaje que se registrará en el log.
    """
    logging.error(mensaje)
