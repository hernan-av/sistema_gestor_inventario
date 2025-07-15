# Módulo de configuración y manejo de logs
# Este módulo se encarga de configurar el registro de logs, 
# creando una carpeta para los archivos de logs y definiendo 
# funciones para registrar mensajes de nivel INFO y ERROR.

import logging
import os
from datetime import datetime

import logging
import os

# Crear carpeta de logs si no existe
LOG_DIR = "."
os.makedirs(LOG_DIR, exist_ok=True)

# Usar un único archivo de log con el nombre fijo "registro.log"
LOG_PATH = os.path.join(LOG_DIR, "registro.log")

# Configuración básica para el logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] → %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, mode='a', encoding="utf-8")]  # Modo 'a' para añadir contenido
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
