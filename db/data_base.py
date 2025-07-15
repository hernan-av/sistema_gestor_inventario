# Módulo para operaciones relacionadas con la base de datos
# Este módulo maneja la creación de tablas, la inicialización de la base de datos 
# y la conexión a la misma para realizar operaciones sobre los datos.

import os
import sqlite3

from core.logger import log_error, log_info

RUTA_DB = "data/inventario.db"

def crear_tablas() -> bool:
    """
    Crea las tablas necesarias en la base de datos si no existen.

    Si la carpeta de la base de datos no existe, la crea automáticamente. 
    Se crean las tablas para categorías, proveedores, productos, clientes, facturas 
    y detalle de facturas.

    Retorna:
        bool: True si la base de datos y las tablas se crearon correctamente, 
            False si ocurrió un error.
    """
    conexion = None
    try:
        # Crear la carpeta si no existe
        os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()

        # Crear tablas en la base de datos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                cuit TEXT NOT NULL UNIQUE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria_id INTEGER,
                proveedor_id INTEGER,
                stock INTEGER DEFAULT 0,
                precio_unitario REAL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id_categoria),
                FOREIGN KEY (proveedor_id) REFERENCES proveedores(id_proveedor)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                dni TEXT NOT NULL UNIQUE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                cliente_id INTEGER,
                nombre_cliente TEXT,
                email_cliente TEXT,
                dni_cliente TEXT,
                total REAL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS factura_detalle (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                precio_unitario REAL,
                total_linea REAL,
                nombre_producto TEXT,
                nombre_categoria TEXT,
                nombre_proveedor TEXT,
                FOREIGN KEY (factura_id) REFERENCES facturas(id_factura),
                FOREIGN KEY (producto_id) REFERENCES productos(id_producto)
            );
        """)

        # Confirmar cambios
        conexion.commit()
        log_info("Base de datos creada correctamente.")
        return True

    except Exception as e:
        log_error(f"Error al crear la base de datos: {e}")
        return False

    finally:
        if conexion:
            conexion.close()


def inicializar_base() -> None:
    """
    Inicializa la base de datos creando las tablas necesarias si no existen.
    Si la creación de las tablas es exitosa, se registra un mensaje de éxito,
    en caso contrario, se registra un error.
    """
    if crear_tablas():
        log_info("Inicialización completada.")
    else:
        log_error("Hubo un problema al iniciar el programa. Verificá el acceso a la base de datos.")


def obtener_conexion():
    """
    Establece y devuelve una conexión activa a la base de datos.

    Configura PRAGMA foreign_keys en ON para habilitar las restricciones de clave externa.

    Retorna:
        conexion: Objeto de conexión a la base de datos SQLite.
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
