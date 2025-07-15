# Módulo de validaciones y gestión de productos
# Este módulo contiene funciones para obtener productos por ID, validar el stock y el precio de productos.

# Imports organizados:
from gestor_productos.productos_db import listar_tabla_producto
from interfaz.diseño_interfaz import mostrar_error

def obtener_producto_por_id_validado(id_str: str):
    """
    Obtiene un producto a partir de su ID si es válido.

    Valida que el ID ingresado sea un número y verifica que exista en la base de datos.

    Parámetros:
        id_str (str): El ID del producto a validar.

    Retorna:
        tuple: El producto correspondiente al ID si existe, None si no.
    """
    if not id_str.isdigit():
        mostrar_error("El ID debe ser un número.")
        return None

    id_producto = int(id_str)

    producto = listar_tabla_producto(id_producto)
    if producto:
        return producto

    mostrar_error("El ID de producto ingresado no existe.")
    return None

def validar_stock(stock_str: str) -> int | None:
    """
    Valida el stock de un producto.

    Verifica que el stock sea un número entero no negativo.

    Parámetros:
        stock_str (str): El stock ingresado para validar.

    Retorna:
        int: El stock como número entero si es válido, None si no lo es.
    """
    try:
        stock = int(stock_str)
        if stock < 0:
            mostrar_error("El stock no puede ser negativo.")
            return None
        return stock
    except ValueError:
        mostrar_error("El stock debe ser un número entero.")
        return None

def validar_precio(precio_str: str) -> float | None:
    """
    Valida el precio unitario de un producto.

    Verifica que el precio sea un número válido y mayor que cero.

    Parámetros:
        precio_str (str): El precio ingresado para validar.

    Retorna:
        float: El precio como número flotante si es válido, None si no lo es.
    """
    try:
        precio = float(precio_str)
        if precio <= 0:
            mostrar_error("El precio debe ser mayor que cero.")
            return None
        return precio
    except ValueError:
        mostrar_error("El precio debe ser un número válido.")
        return None
