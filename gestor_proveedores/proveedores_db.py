# Módulo de operaciones con proveedores
# Este módulo maneja las operaciones de persistencia de proveedores en la base de datos,
# como insertar, modificar, eliminar y listar proveedores.

import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error

def insertar_proveedor(nombre: str, telefono: str, email: str, cuit: str) -> bool:
    """
    Inserta un nuevo proveedor en la base de datos.

    Parámetros:
        nombre (str): El nombre del proveedor.
        telefono (str): El teléfono del proveedor.
        email (str): El email del proveedor.
        cuit (str): El CUIT del proveedor.

    Retorna:
        bool: True si el proveedor fue insertado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO proveedores (nombre, telefono, email, cuit)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, email, cuit))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al insertar proveedor: {e}")
        return False

def modificar_proveedor(id_proveedor: int, nuevo_nombre: str, nuevo_telefono: str, nuevo_email: str, nuevo_cuit: str) -> bool:
    """
    Modifica los datos de un proveedor existente.

    Parámetros:
        id_proveedor (int): ID del proveedor a modificar.
        nuevo_nombre (str): El nuevo nombre del proveedor.
        nuevo_telefono (str): El nuevo teléfono del proveedor.
        nuevo_email (str): El nuevo email del proveedor.
        nuevo_cuit (str): El nuevo CUIT del proveedor.

    Retorna:
        bool: True si el proveedor fue modificado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE proveedores
            SET nombre = ?, telefono = ?, email = ?, cuit = ?
            WHERE id_proveedor = ?
        """, (nuevo_nombre, nuevo_telefono, nuevo_email, nuevo_cuit, id_proveedor))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al modificar proveedor: {e}")
        return False

def eliminar_proveedor(id_proveedor: int) -> bool:
    """
    Elimina un proveedor por su ID.

    Parámetros:
        id_proveedor (int): ID del proveedor a eliminar.

    Retorna:
        bool: True si el proveedor fue eliminado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al eliminar proveedor: {e}")
        return False

def listar_proveedores() -> list:
    """
    Retorna todos los proveedores registrados en la base de datos.

    Retorna:
        list: Lista de tuplas con los datos de los proveedores.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM proveedores ORDER BY id_proveedor ASC")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        log_error(f"Error al listar proveedores: {e}")
        return []
