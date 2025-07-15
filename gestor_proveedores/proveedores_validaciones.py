# Módulo de validaciones y gestión de proveedores
# Este módulo contiene funciones para validar el CUIT de un proveedor, obtener un proveedor por su ID,
# listar proveedores eliminables y verificar si un proveedor tiene productos asociados.

from interfaz.diseño_interfaz import mostrar_error
from gestor_proveedores.proveedores_db import listar_proveedores
from gestor_productos.productos_db import listar_productos_crudos, listar_productos

def validar_cuit(cuit: str, cuit_actual: str = None, permitir_vacio: bool = False) -> bool:
    """
    Valida el CUIT de un proveedor.

    Verifica que el CUIT sea un número de 11 dígitos y que no exista duplicados
    (a menos que sea el mismo CUIT en edición).

    Parámetros:
        cuit (str): El CUIT del proveedor a validar.
        cuit_actual (str): El CUIT actual del proveedor (si es edición).
        permitir_vacio (bool): Si es True, permite que el campo esté vacío (para edición).

    Retorna:
        bool: True si el CUIT es válido, False si no lo es.
    """
    if not cuit:
        if permitir_vacio:
            return True
        else:
            mostrar_error("El CUIT no puede estar vacío.")
            return False

    if not cuit.isdigit() or len(cuit) != 11:
        mostrar_error("El CUIT debe contener 11 dígitos numéricos.")
        return False

    cuits_existentes = []
    for proveedor in listar_proveedores():
        cuits_existentes.append(proveedor[4])

    # Evita rechazar el mismo CUIT en edición
    if cuit_actual is not None and cuit == cuit_actual:
        return True

    if cuit in cuits_existentes:
        mostrar_error("Ya existe un proveedor con ese CUIT.")
        return False

    return True

def obtener_proveedor_por_id_validado(id: str):
    """
    Obtiene un proveedor a partir de su ID si es válido.

    Valida que el ID ingresado sea un número y que exista en la base de datos.

    Parámetros:
        id (str): El ID del proveedor a validar.

    Retorna:
        tuple: El proveedor correspondiente al ID si existe, None si no.
    """
    if not id.isdigit():
        mostrar_error("El ID debe ser un número.")
        return None

    id_proveedor = int(id)
    for proveedor in listar_proveedores():
        if proveedor[0] == id_proveedor:
            return proveedor

    mostrar_error("El ID ingresado no corresponde a ningún proveedor.")
    return None

def listar_proveedores_eliminables() -> list:
    """
    Devuelve una lista de proveedores que no tienen productos asociados.

    Retorna:
        list: Lista de proveedores eliminables (sin productos asociados).
    """
    todos = listar_proveedores()
    productos = listar_productos_crudos()

    proveedores_con_productos = set()
    for producto in productos:
        if producto[3] is not None:  # producto[3] es proveedor_id
            proveedores_con_productos.add(producto[3])

    eliminables = []
    for proveedor in todos:
        if proveedor[0] not in proveedores_con_productos:
            eliminables.append(proveedor)

    return eliminables

def proveedor_tiene_productos(id_proveedor: int) -> bool:
    """
    Devuelve True si el proveedor tiene al menos un producto asociado.

    Parámetros:
        id_proveedor (int): ID del proveedor a verificar.

    Retorna:
        bool: True si el proveedor tiene productos asociados, False si no.
    """
    productos = listar_productos()
    for producto in productos:
        if producto[3] == int(id_proveedor):  # producto[3] es proveedor_id
            return True
    return False
