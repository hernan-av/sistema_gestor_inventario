# Módulo de utilidades para fechas y texto
# Funciones para obtener la fecha actual y formatear texto.

from datetime import datetime
import unicodedata

def obtener_fecha_actual():
    """
    Retorna la fecha y hora actual en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def normalizar_texto(texto: str) -> str:
    """
    Normaliza el texto a minúsculas y elimina acentos.
    """
    return unicodedata.normalize("NFKD", texto.strip().lower()).encode("ASCII", "ignore").decode("utf-8")

def formatear_nombre(texto: str) -> str:
    """
    Capitaliza el nombre (primera letra de cada palabra).
    """
    return texto.strip().title()

def formatear_email(texto: str) -> str:
    """
    Convierte el correo a minúsculas.
    """
    return texto.strip().lower()

