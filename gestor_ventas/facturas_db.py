# Módulo de operaciones con facturas
# Este módulo maneja las operaciones de persistencia de facturas en la base de datos,
# como insertar facturas, insertar los detalles de las facturas, descontar stock y listar facturas.

import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error

def insertar_factura(fecha: str, cliente_id: int, total: float, conexion: sqlite3.Connection) -> int | None:
    """
    Inserta una nueva factura en la base de datos.

    Parámetros:
        fecha (str): La fecha de la factura.
        cliente_id (int): El ID del cliente asociado a la factura.
        total (float): El total de la factura.
        conexion (sqlite3.Connection): Conexión a la base de datos.

    Retorna:
        int: El ID de la factura recién insertada, o None si hubo un error.
    """
    try:
        cursor = conexion.cursor()

        # Obtener datos congelados del cliente
        cursor.execute("SELECT nombre, email, dni FROM clientes WHERE id_cliente = ?", (cliente_id,))
        cliente = cursor.fetchone()
        if not cliente:
            raise ValueError("Cliente no encontrado.")
        cliente_nombre, cliente_email, cliente_dni = cliente

        cursor.execute("""
            INSERT INTO facturas (fecha, cliente_id, nombre_cliente, email_cliente, dni_cliente, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fecha, cliente_id, cliente_nombre, cliente_email, cliente_dni, total))

        return cursor.lastrowid

    except sqlite3.Error as e:
        log_error(f"Error al insertar factura: {e}")
        return None

def insertar_factura_detalle(factura_id: int, producto_id: int, cantidad: int, precio_unitario: float, total_linea: float, conexion: sqlite3.Connection):
    """
    Inserta un detalle de factura en la base de datos.

    Parámetros:
        factura_id (int): El ID de la factura a la que pertenece el detalle.
        producto_id (int): El ID del producto en la factura.
        cantidad (int): La cantidad de productos en el detalle.
        precio_unitario (float): El precio unitario del producto.
        total_linea (float): El total de la línea de factura (cantidad * precio unitario).
        conexion (sqlite3.Connection): Conexión a la base de datos.
    """
    try:
        cursor = conexion.cursor()

        # Obtener datos congelados del producto, categoría y proveedor
        cursor.execute("""
            SELECT p.nombre, c.nombre, pr.nombre
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id_categoria
            JOIN proveedores pr ON p.proveedor_id = pr.id_proveedor
            WHERE p.id_producto = ?
        """, (producto_id,))
        resultado = cursor.fetchone()
        if not resultado:
            raise ValueError("Producto, categoría o proveedor no encontrados.")
        producto_nombre, categoria_nombre, proveedor_nombre = resultado

        cursor.execute("""
            INSERT INTO factura_detalle (
                factura_id, producto_id, cantidad, precio_unitario, total_linea,
                nombre_producto, nombre_categoria, nombre_proveedor
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            factura_id, producto_id, cantidad, precio_unitario, total_linea,
            producto_nombre, categoria_nombre, proveedor_nombre
        ))
    except sqlite3.Error as e:
        log_error(f"Error al insertar detalle de factura: {e}")
        return None

def descontar_stock(producto_id: int, cantidad: int, conexion: sqlite3.Connection):
    """
    Descuenta la cantidad de un producto en el inventario.

    Parámetros:
        producto_id (int): El ID del producto al que se le va a descontar stock.
        cantidad (int): La cantidad de productos a descontar del inventario.
        conexion (sqlite3.Connection): Conexión a la base de datos.
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos SET stock = stock - ? WHERE id_producto = ?
        """, (cantidad, producto_id))
    except sqlite3.Error as e:
        log_error(f"Error al descontar stock: {e}")

def listar_facturas() -> list:
    """
    Retorna todas las facturas registradas en la base de datos.

    Retorna:
        list: Lista de tuplas con los detalles de las facturas.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                f.id_factura,
                f.fecha,
                f.nombre_cliente,
                f.total 
            FROM facturas f
            ORDER BY fecha DESC
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        log_error(f"Error al listar facturas: {e}")
        return []
    finally:
        if conexion:
            conexion.close()

def obtener_detalle_venta(id_factura: int) -> list:
    """
    Obtiene el detalle de una venta a partir de su ID de factura.

    Parámetros:
        id_factura (int): El ID de la factura para la cual se quiere obtener el detalle.

    Retorna:
        list: Detalles de la factura y sus productos asociados.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                f.id_factura,
                f.fecha,
                f.cliente_id,
                f.nombre_cliente,
                f.email_cliente,
                f.dni_cliente,
                fd.producto_id,
                fd.nombre_producto,
                fd.nombre_categoria,
                fd.cantidad,
                fd.precio_unitario,
                fd.total_linea,
                f.total
            FROM facturas f
            JOIN factura_detalle fd ON fd.factura_id = f.id_factura
            WHERE f.id_factura = ?
        """, (id_factura,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        log_error(f"Error al obtener detalle de venta: {e}")
        return []
    finally:
        if conexion:
            conexion.close()
