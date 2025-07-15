# Módulo de operaciones con clientes
# Este módulo maneja las operaciones de persistencia de clientes en la base de datos,
# como insertar, modificar, eliminar y listar clientes, incluyendo la lista de clientes
# sin facturas asociadas.

import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error

def insertar_cliente(nombre: str, telefono: str, email: str, dni: str) -> bool:
    """
    Inserta un nuevo cliente en la base de datos.

    Parámetros:
        nombre (str): El nombre del cliente.
        telefono (str): El teléfono del cliente.
        email (str): El email del cliente.
        dni (str): El DNI del cliente.

    Retorna:
        bool: True si el cliente fue insertado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, telefono, email, dni)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, email, dni))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al insertar cliente: {e}")
        return False

def modificar_cliente(id_cliente: int, nuevo_nombre: str, nuevo_telefono: str, nuevo_email: str, nuevo_dni: str) -> bool:
    """
    Modifica los datos de un cliente existente.

    Parámetros:
        id_cliente (int): El ID del cliente a modificar.
        nuevo_nombre (str): El nuevo nombre del cliente.
        nuevo_telefono (str): El nuevo teléfono del cliente.
        nuevo_email (str): El nuevo email del cliente.
        nuevo_dni (str): El nuevo DNI del cliente.

    Retorna:
        bool: True si los datos del cliente fueron modificados correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, email = ?, dni = ?
            WHERE id_cliente = ?
        """, (nuevo_nombre, nuevo_telefono, nuevo_email, nuevo_dni, id_cliente))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al modificar cliente: {e}")
        return False

def eliminar_cliente(id_cliente: int) -> bool:
    """
    Elimina un cliente por su ID.

    Parámetros:
        id_cliente (int): El ID del cliente a eliminar.

    Retorna:
        bool: True si el cliente fue eliminado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al eliminar cliente: {e}")
        return False

def listar_clientes() -> list:
    """
    Retorna todos los clientes registrados en la base de datos.

    Retorna:
        list: Lista de tuplas con los datos de los clientes.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY id_cliente ASC")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        log_error(f"Error al listar clientes: {e}")
        return []

def listar_clientes_sin_facturas() -> list:
    """
    Retorna los clientes que NO tienen facturas asociadas.

    Esta función es útil para procesos de eliminación segura de clientes que no tienen 
    transacciones registradas.

    Retorna:
        list: Lista de tuplas con los datos de los clientes sin facturas asociadas.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT c.id_cliente, c.nombre, c.telefono, c.email, c.dni
            FROM clientes c
            LEFT JOIN facturas f ON c.id_cliente = f.cliente_id
            WHERE f.cliente_id IS NULL
            ORDER BY c.id_cliente ASC
        """)

        resultados = cursor.fetchall()
        return resultados

    except sqlite3.Error as e:
        log_error(f"Error al listar clientes sin facturas: {e}")
        return []

    finally:
        if conexion:
            conexion.close()
