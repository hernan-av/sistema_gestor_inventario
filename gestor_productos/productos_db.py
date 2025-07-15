# Módulo de operaciones con productos
# Este módulo maneja las operaciones de persistencia de productos en la base de datos,
# como insertar, modificar, eliminar, y listar productos.

import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error

def insertar_producto(nombre: str, categoria_id: int, proveedor_id: int, stock: int, precio_unitario: float) -> bool:
    """
    Inserta un nuevo producto en la base de datos.

    Parámetros:
        nombre (str): Nombre del producto.
        categoria_id (int): ID de la categoría del producto.
        proveedor_id (int): ID del proveedor del producto.
        stock (int): Cantidad de producto en inventario.
        precio_unitario (float): Precio unitario del producto.

    Retorna:
        bool: True si el producto fue insertado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, categoria_id, proveedor_id, stock, precio_unitario)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, categoria_id, proveedor_id, stock, precio_unitario))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al insertar producto: {e}")
        return False

def modificar_producto(id_producto: int, nuevo_nombre: str, nueva_categoria: int, nuevo_proveedor: int, nuevo_stock: int, nuevo_precio: float) -> bool:
    """
    Modifica los datos de un producto existente por su ID.

    Parámetros:
        id_producto (int): ID del producto a modificar.
        nuevo_nombre (str): Nuevo nombre del producto.
        nueva_categoria (int): Nueva categoría del producto.
        nuevo_proveedor (int): Nuevo proveedor del producto.
        nuevo_stock (int): Nuevo stock del producto.
        nuevo_precio (float): Nuevo precio del producto.

    Retorna:
        bool: True si el producto fue modificado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, categoria_id = ?, proveedor_id = ?, stock = ?, precio_unitario = ?
            WHERE id_producto = ?
        """, (nuevo_nombre, nueva_categoria, nuevo_proveedor, nuevo_stock, nuevo_precio, id_producto))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al modificar producto: {e}")
        return False

def eliminar_producto(id_producto: int) -> bool:
    """
    Elimina un producto de la base de datos por su ID.

    Parámetros:
        id_producto (int): ID del producto a eliminar.

    Retorna:
        bool: True si el producto fue eliminado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al eliminar producto: {e}")
        return False

def listar_productos() -> list:
    """
    Retorna una lista de productos con nombres de categoría y proveedor.

    Retorna:
        list: Lista de productos con información adicional de categoría y proveedor.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                p.id_producto,
                p.nombre,
                c.nombre AS categoria,
                prov.nombre AS proveedor,
                p.stock,
                p.precio_unitario
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id_categoria
            JOIN proveedores prov ON p.proveedor_id = prov.id_proveedor
            ORDER BY p.id_producto ASC
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        log_error(f"Error al listar productos: {e}")
        return []

def listar_tabla_producto(id_producto: int):
    """
    Devuelve el producto puro desde la tabla 'productos', sin JOIN ni campos externos.

    Parámetros:
        id_producto (int): El ID del producto a consultar.

    Retorna:
        tuple: El producto correspondiente al ID si existe, None si no existe.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado
    except sqlite3.Error as e:
        log_error(f"Error al consultar producto directo: {e}")
        return None

def listar_productos_crudos() -> list:
    """
    Devuelve todos los productos sin JOIN (directo desde tabla productos).

    Retorna:
        list: Lista de todos los productos directamente desde la tabla sin información adicional.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id_producto ASC")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        log_error(f"Error al listar productos: {e}")
        return []
