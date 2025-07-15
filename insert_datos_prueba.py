import sqlite3

from db.data_base import obtener_conexion
from core.logger import log_error, log_info

def insertar_datos_prueba() -> bool:
    """
    Inserta datos de prueba en las tablas de categorías, proveedores, productos y clientes.
    
    Retorna:
        bool: True si los datos fueron insertados correctamente, 
            False si ocurrió un error.
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Insertar categorías de prueba
        categorias = [
            ("Periféricos"),
            ("Computadoras"),
            ("Sonido"),
            ("Accesorios"),
            ("Pantallas"),
            ("Redes"),
            ("Almacenamiento"),
            ("Cámaras"),
            ("Micrófonos"),
            ("Conectividad")
        ]
        cursor.executemany("INSERT OR IGNORE INTO categorias (nombre) VALUES (?)", [(categoria,) for categoria in categorias])

        # Insertar proveedores de prueba
        proveedores = [
            ("TechDistrib SA", "1150001000", "ventas@techdistrib.com", "30548976123"),
            ("PixelTrade SRL", "1144003000", "info@pixeltrade.com", "30765432987"),
            ("ZendaTech", "1166004000", "contacto@zendatech.com", "30548911223"),
            ("NovaElectro SA", "1177005000", "ventas@novaelectro.com", "30784291425"),
            ("ElectroNet SRL", "1133006000", "soporte@electronet.com", "30698754123"),
            ("Neotec Supplies", "1188007000", "pedidos@neotec.com", "30712549876"),
            ("MasterTech", "1122008000", "ventas@mastertech.com", "30678912345"),
            ("BitImport SRL", "1140009000", "compras@bitimport.com", "30789654123"),
            ("CoreByte SRL", "1155001001", "contacto@corebyte.com", "30565498741"),
            ("SysDistrib SA", "1170001100", "info@sysdistrib.com", "30874123698")
        ]
        cursor.executemany("INSERT OR IGNORE INTO proveedores (nombre, telefono, email, cuit) VALUES (?, ?, ?, ?)", proveedores)

        # Insertar clientes de prueba
        clientes = [
            ("Laura Martínez", "1123456789", "laura.martinez@mail.com", "40875231"),
            ("Ricardo Gómez", "1134567890", "ricardo.gomez@mail.com", "39548620"),
            ("Daniela Torres", "1145678901", "daniela.torres@mail.com", "42319876"),
            ("Javier Ruiz", "1156789012", "javier.ruiz@mail.com", "38765412"),
            ("Sofía Fernández", "1167890123", "sofia.fernandez@mail.com", "41098567"),
            ("Mateo Navarro", "1178901234", "mateo.navarro@mail.com", "40234687"),
            ("Valentina Díaz", "1189012345", "valentina.diaz@mail.com", "41687452"),
            ("Nicolás Romero", "1190123456", "nicolas.romero@mail.com", "42985741"),
            ("Martina López", "1132145678", "martina.lopez@mail.com", "41987654"),
            ("Tomás Herrera", "1143256789", "tomas.herrera@mail.com", "43127841")
        ]
        cursor.executemany("INSERT OR IGNORE INTO clientes (nombre, telefono, email, dni) VALUES (?, ?, ?, ?)", clientes)

        # Insertar productos de prueba
        productos = [
            ("Teclado mecánico RGB", 1, 1, 25, 90500),
            ("Mouse inalámbrico", 1, 2, 40, 27800),
            ("Auriculares gamer", 3, 3, 30, 89000),
            ("Monitor LED 24\"", 5, 4, 15, 344500),
            ("Laptop Intel i5 8GB SSD", 2, 5, 10, 1200500),
            ("Parlantes Bluetooth", 3, 1, 35, 76000),
            ("Alfombrilla XL antideslizante", 4, 6, 50, 22700),
            ("Micrófono USB condensador", 9, 2, 20, 68000),
            ("Webcam Full HD 1080p", 8, 3, 20, 85000),
            ("Hub USB 4 puertos", 10, 7, 18, 37000)
        ]
        cursor.executemany("INSERT OR IGNORE INTO productos (nombre, categoria_id, proveedor_id, stock, precio_unitario) VALUES (?, ?, ?, ?, ?)", productos)

        # Confirmar cambios
        conexion.commit()
        log_info("Datos de prueba insertados correctamente.")
        return True
    except Exception as e:
        log_error(f"Error al insertar datos de prueba: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    insertar_datos_prueba()
    print("Datos de prueba insertados correctamente.")
