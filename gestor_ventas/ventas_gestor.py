# Módulo de gestión de ventas
# Este módulo maneja las operaciones de ventas, incluyendo el registro de ventas, la validación de productos,
# y la exportación de facturas a PDF, además de interactuar con el usuario para confirmar las ventas.

from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

from db.data_base import obtener_conexion
from gestor_clientes.clientes_db import listar_clientes
from gestor_productos.productos_db import listar_productos_crudos, listar_productos
from gestor_ventas.facturas_db import insertar_factura, insertar_factura_detalle, descontar_stock, obtener_detalle_venta, listar_facturas
from gestor_proveedores.proveedores_validaciones import obtener_proveedor_por_id_validado
from gestor_ventas.ventas_validaciones import cargar_productos_para_venta
from gestor_ventas.exportar_factura import generar_pdf_factura
from gestor_clientes.clientes_validaciones import obtener_cliente_por_id_validado
from gestor_categorias.categorias_validaciones import obtener_categoria_por_id_validado
from interfaz.mostrar_resumen import mostrar_clientes,mostrar_facturas, mostrar_resumen_venta
from interfaz.diseño_interfaz import mostrar_error,mostrar_exito, mostrar_cancelado, mostrar_info
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from core.utils import obtener_fecha_actual
from core.logger import log_info, log_error

def registrar_venta(cliente_id: int, productos: list[dict]) -> int | None:
    """
    Registra una venta en el sistema.

    Provee los datos para los insert y actualizacion de stock en la base de datos

    Parámetros:
        cliente_id (int): El ID del cliente que realiza la compra.
        productos (list[dict]): Lista de diccionarios que contienen la información de los productos a vender.

    Retorna:
        int: El ID de la factura si la venta se realizó correctamente, o None en caso de error.
    """
    fecha = obtener_fecha_actual()
    conexion = obtener_conexion()

    try:
        # Iniciar transacción
        conexion.execute("BEGIN TRANSACTION;")
        
        # Validar cliente
        cliente = obtener_cliente_por_id_validado(str(cliente_id))
        if not cliente:
            mostrar_error("Cliente no encontrado.")
            conexion.rollback()
            return None

        # Construir diccionario de productos desde base
        productos_db = {}
        for prod in listar_productos_crudos():
            productos_db[prod[0]] = {
                "nombre": prod[1],
                "categoria_id": prod[2],
                "proveedor_id": prod[3],
                "stock": prod[4],
                "precio_unitario": prod[5]
            }

        total_factura = 0
        detalles = []

        for item in productos:
            pid = item["producto_id"]
            cantidad = item["cantidad"]

            if pid not in productos_db:
                mostrar_error(f"Producto con ID {pid} no encontrado.")
                conexion.rollback()
                return None

            producto_info = productos_db[pid]
            precio = producto_info["precio_unitario"]
            subtotal = round(cantidad * precio, 2)
            total_factura += subtotal

            # Validar vínculos
            if not obtener_categoria_por_id_validado(str(producto_info["categoria_id"])):
                mostrar_error(f"Categoría no encontrada para '{producto_info['nombre']}'.")
                conexion.rollback()
                return None

            if not obtener_proveedor_por_id_validado(str(producto_info["proveedor_id"])):
                mostrar_error(f"Proveedor no encontrado para '{producto_info['nombre']}'.")
                conexion.rollback()
                return None

            detalles.append({
                "producto_id": pid,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "total_linea": subtotal
            })

        # Insertar factura y detalle de factura en una única transacción
        factura_id = insertar_factura(fecha, cliente_id, total_factura, conexion)
        if factura_id is None:
            mostrar_error("No se pudo insertar la factura.")
            conexion.rollback()
            return None

        for detalle in detalles:
            insertar_factura_detalle(
                factura_id,
                detalle["producto_id"],
                detalle["cantidad"],
                detalle["precio_unitario"],
                detalle["total_linea"],
                conexion
            )
            descontar_stock(detalle["producto_id"], detalle["cantidad"], conexion)  # Descontar el stock

        # Confirmar cambios
        conexion.commit()
        log_info(f"Venta completada → Cliente ID: {cliente_id}, Factura ID: {factura_id}, Total: ${total_factura:.2f}")
        return factura_id

    except Exception as e:
        conexion.rollback()
        log_error(f"Error al registrar la venta: {e}")
        mostrar_error(f"Ocurrió un error al registrar la venta.")
        return None

    finally:
        conexion.close()

def procesar_venta_interactiva():
    """
    Permite procesar una venta de manera interactiva, donde el usuario puede seleccionar un cliente
    y productos, ver el resumen y confirmar la venta.

    Este proceso también genera la factura correspondiente y la exporta a PDF.
    """
    clientes = listar_clientes()
    if not clientes:
        mostrar_error("No hay clientes registrados. Ingresa al nuevo cliente y luego reintenta la venta.\n")
        return

    mostrar_clientes(clientes)
    mostrar_info("Si el cliente no existe, primero crealo y luego reintenta la venta")

    # Selección de cliente
    while True:
        cliente_id = pedir_input_con_cancelacion("Ingresá el ID del cliente para la venta (C para cancelar): ")
        if cliente_id.lower() == "c":
            mostrar_cancelado("Ventas")
            return

        cliente = obtener_cliente_por_id_validado(cliente_id)
        if cliente is None:
            continue
        break

    # Carga de productos
    productos = cargar_productos_para_venta()
    if productos == "CANCELADO":
        return

    # Mostrar resumen previo a confirmar la venta
    productos_db = listar_productos()
    productos_dict = {}
    for prod in productos_db:
        productos_dict[prod[0]] = {
            "nombre": prod[1],
            "precio_unitario": prod[5]
        }

    console = Console()
    console.print()
    console.print(Rule(" Resumen venta a confirmar ", style="grey39"))
    console.print()

    # Panel izquierdo: productos seleccionados
    lineas = []
    total_final = 0
    for item in productos:
        pid = item["producto_id"]
        nombre = productos_dict[pid]["nombre"]
        precio_unit = productos_dict[pid]["precio_unitario"]
        cantidad = item["cantidad"]
        subtotal = cantidad * precio_unit
        total_final += subtotal

        linea = f"[bold green]{nombre}[/] — {cantidad} un. × ${precio_unit:.2f} → ${subtotal:.2f}"
        lineas.append(linea)

    contenido_venta = "\n".join(lineas)
    panel_venta = Panel(contenido_venta, title=Text("Productos seleccionados", style="bold green"), border_style="grey39", padding=(0, 2))

    # Panel derecho: total final
    panel_total = Panel.fit(
        f"[bold green]TOTAL:[/] ${total_final:.2f}",
        title=Text("Importe final", style="bold green"),
        border_style="grey39",
        padding=(0, 2)
    )

    # Mostrar paneles lado a lado
    console.print(Columns([panel_venta, panel_total], equal=True))

    # Confirmación
    respuesta = pedir_input_con_cancelacion("¿Deseás confirmar esta venta? (S para confirmar, otra tecla para cancelar): ")
    if respuesta.lower() != "s":
        mostrar_cancelado("Ventas")
        return

    # Registrar venta
    factura_id = registrar_venta(cliente_id, productos)
    if factura_id is None:
        mostrar_error("No se pudo registrar la venta\n")
        return

    mostrar_resumen_venta(factura_id)
    ruta = generar_pdf_factura(factura_id)
    mostrar_exito(f"Factura guardada en: {ruta}")

def imprimir_detalle_venta():
    """
    Imprime en consola el detalle de una factura al consultarla.

    Permite al usuario ingresar un ID de factura y muestra todos los productos y detalles asociados.
    """
    lista_facturas = listar_facturas()
    if not lista_facturas:
        mostrar_error("No hay facturas registradas.\n")
        return

    mostrar_facturas(lista_facturas)

    while True:
        entrada = pedir_input_con_cancelacion("Ingresá el ID de la factura para ver el detalle (C para cancelar): ")
        if entrada.lower() == "c":
            mostrar_cancelado("Ventas")
            return

        try:
            id_factura = int(entrada)
        except ValueError:
            mostrar_error("El ID debe ser un número.")
            continue

        ids_disponibles = []
        for fact in lista_facturas:
            ids_disponibles.append(fact[0])
        if id_factura not in ids_disponibles:
            mostrar_error("El ID de factura no existe.")
            continue

        break  # ID válido

    detalle = obtener_detalle_venta(id_factura)
    mostrar_resumen_venta(id_factura)
    return detalle
