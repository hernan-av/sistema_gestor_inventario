# Módulo de operaciones con categorías
# Este módulo contiene funciones para insertar, modificar, eliminar y listar categorías
# en la base de datos de inventario.

import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error

def insertar_categoria(nombre: str) -> bool:
    """
    Inserta una nueva categoría en la base de datos.

    Parámetros:
        nombre (str): El nombre de la categoría a insertar.

    Retorna:
        bool: True si la categoría se insertó correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al insertar categoría: {e}")
        return False

def modificar_categoria(id_categoria: int, nuevo_nombre: str) -> bool:
    """
    Modifica el nombre de una categoría existente por su ID.

    Parámetros:
        id_categoria (int): El ID de la categoría que se desea modificar.
        nuevo_nombre (str): El nuevo nombre para la categoría.

    Retorna:
        bool: True si la categoría fue modificada correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE categorias SET nombre = ? WHERE id_categoria = ?", (nuevo_nombre, id_categoria))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al modificar categoría: {e}")
        return False

def eliminar_categoria(id_categoria: int) -> bool:
    """
    Elimina una categoría por su ID.

    Parámetros:
        id_categoria (int): El ID de la categoría a eliminar.

    Retorna:
        bool: True si la categoría fue eliminada correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        log_error(f"Error al eliminar categoría: {e}")
        return False

def listar_categorias() -> list:
    """
    Retorna todas las categorías registradas en la base de datos.

    Retorna:
        list: Una lista de tuplas con las categorías, o una lista vacía en caso de error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM categorias ORDER BY id_categoria ASC")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        log_error(f"Error al listar categorías: {e}")
        return []
