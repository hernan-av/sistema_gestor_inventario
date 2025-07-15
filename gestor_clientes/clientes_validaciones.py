# Módulo de validaciones de clientes
# Este módulo contiene funciones para validar datos de clientes, obtener clientes por ID
# y determinar si un cliente puede ser eliminado.

import re

from interfaz.diseño_interfaz import mostrar_error
from gestor_clientes.clientes_db import listar_clientes, listar_clientes_sin_facturas
from gestor_ventas.facturas_db import listar_facturas

def validar_dni(dni: str, dni_actual: str = None, permitir_vacio: bool = False) -> bool:
    """
    Verifica que el DNI no esté vacío, que sea un número y que tenga entre 6 y 8 dígitos.
    Además, verifica duplicidad (a menos que sea el DNI actual en edición).

    Parámetros:
        dni (str): El DNI del cliente a validar.
        dni_actual (str): El DNI actual del cliente (si es edición).
        permitir_vacio (bool): Si es True, permite que el campo esté vacío (para edición).

    Retorna:
        bool: True si el DNI es válido, False si no lo es.
    """
    if not dni:
        if permitir_vacio:
            return True  # Se permite mantener vacío (por ejemplo, Enter para dejar igual en edición)
        else:
            mostrar_error("El DNI no puede estar vacío")
            return False

    if not dni.isdigit() or not (6 <= len(dni) <= 8):
        mostrar_error("El DNI debe contener entre 6 y 8 dígitos numéricos")
        return False

    dnis_existentes = []
    for clientes in listar_clientes():
        dnis_existentes.append(clientes[4])

    # Evita rechazar el mismo DNI en edición
    if dni_actual is not None and dni == dni_actual:
        return True

    if dni in dnis_existentes:
        mostrar_error("Ya existe un cliente con ese DNI")
        return False

    return True

def validar_nombre_cliente(nombre: str, permitir_vacio: bool = False) -> bool:
    """
    Valida que el nombre de un cliente no esté vacío y contenga solo letras y espacios.

    Parámetros:
        nombre (str): El nombre del cliente a validar.
        permitir_vacio (bool): Si es True, permite que el campo esté vacío (para edición).

    Retorna:
        bool: True si el nombre es válido, False si no lo es.
    """
    if not nombre:
        if permitir_vacio:
            return True  # Se permite vacío (para edición)
        mostrar_error("El nombre no puede estar vacío")
        return False

    # Validar que el nombre contenga solo letras y espacios
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
        mostrar_error("El nombre solo puede contener letras y espacios.")
        return False
    
    return True

def obtener_cliente_por_id_validado(id: str):
    """
    Obtiene un cliente a partir de su ID si es válido.

    Valida que el ID sea numérico y existe en la base de datos de clientes.

    Parámetros:
        id (str): El ID del cliente a validar.

    Retorna:
        tuple: El cliente correspondiente al ID si existe, None si no.
    """
    if not id.isdigit():
        mostrar_error("El ID debe ser un número")
        return None

    id_cliente = int(id)
    encontrado = False
    for cliente in listar_clientes():
        if cliente[0] == id_cliente:
            encontrado = True
            return cliente

    if not encontrado:
        mostrar_error("El ID de cliente ingresado no existe")
        return None

def listar_clientes_eliminables() -> list:
    """
    Devuelve una lista de clientes que no tienen facturas asociadas y pueden ser eliminados.

    Revisa las categorías que no tienen productos vinculados a ellas en la base de datos.

    Retorna:
        list: Lista de clientes que pueden ser eliminados.
    """
    todos = listar_clientes_sin_facturas()
    facturas = listar_facturas()

    # Obtener IDs de clientes que tienen facturas
    clientes_con_factura = set()
    for factura in facturas:
        cliente_id = factura[2]
        if cliente_id is not None:
            clientes_con_factura.add(cliente_id)

    # Filtrar clientes que no están en la lista de los que tienen facturas
    eliminables = []
    for cliente in todos:
        id_cliente = cliente[0]
        if id_cliente not in clientes_con_factura:
            eliminables.append(cliente)

    return eliminables