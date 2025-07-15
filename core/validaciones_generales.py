# Módulo de validaciones generales
# Este módulo contiene funciones para validar los campos de entrada comunes en el sistema:
# nombre, teléfono y correo electrónico.

from interfaz.diseño_interfaz import mostrar_error

def validar_nombre(nombre: str, permitir_vacio: bool = False) -> bool:
    """
    Valida que el nombre no esté vacío.

    Si se permite vacío (en el caso de edición) para conservar valor actual.

    Parámetros:
        nombre (str): El nombre a validar.
        permitir_vacio (bool): Si es True, permite que el nombre esté vacío.

    Retorna:
        bool: True si el nombre es válido, False en caso contrario.
    """
    if not nombre:
        if permitir_vacio:
            return True  # se considera válido si se permite vacío (en edición)
        mostrar_error("El nombre no puede estar vacío")
        return False
    return True

def validar_telefono(telefono: str, permitir_vacio: bool = False) -> bool:
    """
    Valida que el teléfono sea un número y no esté vacío.

    Si se permite vacío (en el caso de edición) para conservar valor actual.

    Parámetros:
        telefono (str): El número de teléfono a validar.
        permitir_vacio (bool): Si es True, permite que el teléfono esté vacío.

    Retorna:
        bool: True si el teléfono es válido, False en caso contrario.
    """
    if not telefono:
        if permitir_vacio:
            return True
        mostrar_error("El teléfono no puede estar vacío")
        return False
    if not telefono.isdigit():
        mostrar_error("El teléfono solo puede contener números")
        return False
    return True

def validar_email(email: str, permitir_vacio: bool = False) -> bool:
    """
    Valida que el correo electrónico tenga un formato correcto.

    Si se permite vacío (en el caso de edición) para conservar valor actual.

    Parámetros:
        email (str): El correo electrónico a validar.
        permitir_vacio (bool): Si es True, permite que el correo esté vacío.

    Retorna:
        bool: True si el email es válido, False en caso contrario.
    """
    if not email:
        if permitir_vacio:
            return True
        mostrar_error("El email no puede estar vacío")
        return False
    if "@" not in email or "." not in email:
        mostrar_error("El formato del email no es válido")
        return False
    return True
