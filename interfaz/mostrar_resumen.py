# Módulo Rich para consola y elementos visuales

from rich.console import Console
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table

from interfaz.diseño_interfaz import mostrar_error
from gestor_ventas.facturas_db import obtener_detalle_venta


console = Console()


def mostrar_productos(productos: list):
    """
    Muestra una tabla con los productos disponibles en el sistema.

    Args:
        productos (list): Lista de productos a mostrar.
    """
    console.print()
    titulo_tabla = Text("Productos disponibles", style="white")
    tabla = Table(title=titulo_tabla, header_style="bold green", border_style="grey39", show_lines=False)
    tabla.add_column("ID", style="white", justify="center")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Categoría", style="white")
    tabla.add_column("Proveedor", style="white")
    tabla.add_column("Stock", style="white", justify="center")
    tabla.add_column("Precio Venta", style="white", justify="right")

    for prod in productos:
        tabla.add_row(str(prod[0]), str(prod[1]), str(prod[2]), str(prod[3]), str(prod[4]), f"${prod[5]:.2f}")
    
    console.print(tabla)
    console.print()

def mostrar_proveedores(proveedores: list):
    """
    Muestra una tabla con los proveedores registrados.

    Args:
        proveedores (list): Lista de proveedores a mostrar.
    """
    console.print()
    titulo_tabla = Text("Proveedores registrados", style="white")
    tabla = Table(title=titulo_tabla, header_style="bold green", border_style="grey39", show_lines=False)
    tabla.add_column("ID", style="white", justify="center")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Teléfono", style="white", justify="center")
    tabla.add_column("Email", style="white")
    tabla.add_column("CUIT", style="white", justify="center")

    for prov in proveedores:
        tabla.add_row(str(prov[0]), prov[1], prov[2], prov[3], prov[4])
    
    console.print(tabla)
    console.print()

def mostrar_categorias(categorias: list):
    """
    Muestra una tabla con las categorías existentes.

    Args:
        categorias (list): Lista de categorías a mostrar.
    """
    console.print()
    titulo_tabla = Text("Categorías existentes", style="white")
    tabla = Table(title=titulo_tabla, header_style="bold green", border_style="grey39", show_lines=False)
    tabla.add_column("ID", style="white", justify="center")
    tabla.add_column("Nombre", style="white")

    for cat in categorias:
        tabla.add_row(str(cat[0]), cat[1])
    
    console.print(tabla)
    console.print()

def mostrar_clientes(clientes: list):
    """
    Muestra una tabla con los clientes registrados.

    Args:
        clientes (list): Lista de clientes a mostrar.
    """
    console.print()
    titulo_tabla = Text("Clientes registrados", style="white")
    tabla = Table(title=titulo_tabla, header_style="bold green", border_style="grey39", show_lines=False)
    tabla.add_column("ID", style="white", justify="center")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Teléfono", style="white", justify="center")
    tabla.add_column("Email", style="white")
    tabla.add_column("DNI", style="white", justify="center")

    for cli in clientes:
        tabla.add_row(str(cli[0]), cli[1], cli[2], cli[3], cli[4])
    
    console.print(tabla)
    console.print()

def mostrar_facturas(facturas: list):
    """
    Muestra una tabla con las facturas generadas.

    Args:
        facturas (list): Lista de facturas a mostrar.
    """
    if not facturas:
        mostrar_error("No hay facturas registradas\n")
        return

    console.print()
    titulo_tabla = Text("Facturas generadas", style="white")
    tabla = Table(title=titulo_tabla, header_style="bold green", border_style="grey39", show_lines=False)
    tabla.add_column("ID", justify="center", style="white")
    tabla.add_column("Fecha", style="white", justify="center")
    tabla.add_column("Cliente", style="white")
    tabla.add_column("Total", justify="right", style="white")

    for fac in facturas:
        tabla.add_row(str(fac[0]), fac[1], str(fac[2]), f"${fac[3]:.2f}")
    
    console.print(tabla)
    console.print()

def mostrar_resumen_venta(id_factura: int):
    """
    Muestra un resumen detallado de la venta para la factura especificada.

    Args:
        id_factura (int): ID de la factura a mostrar.
    """
    detalle = obtener_detalle_venta(id_factura)
    if not detalle:
        mostrar_error("No se encontró la factura especificada\n")
        return

    (_, fecha, cliente_id, cliente_nombre, email, dni, _, _, _, _, _, _, total_factura) = detalle[0]

    console.print()
    console.print(Rule(" Detalle factura ", style="grey39"))
    console.print()

    # Panel de factura
    panel_factura = Panel.fit(
        f"[bold green]Factura #[/] {id_factura}\n"
        f"[bold green]Fecha:[/] {fecha}\n"
        f"[bold green]Total:[/] ${total_factura:.2f}",
        border_style="grey39",
        padding=(0, 2)
    )

    # Panel de cliente
    panel_cliente = Panel.fit(
        f"[bold green]Cliente:[/] {cliente_nombre}\n"
        f"[bold green]ID Cliente:[/] {cliente_id}\n"
        f"[bold green]Email:[/] {email}\n"
        f"[bold green]DNI:[/] {dni}",
        border_style="grey39",
        padding=(0, 2)
    )

    # Mostrar paneles lado a lado
    console.print(Columns([panel_factura, panel_cliente], equal=True))
    console.print()

    # Tabla de productos vendidos
    titulo_tabla = Text("Detalle de productos vendidos", style="white")

    tabla = Table(
        title=titulo_tabla,
        show_lines=False,
        header_style="bold green",
        border_style="grey39"
    )
    tabla.add_column("Producto", style="white", justify="left")
    tabla.add_column("Categoría", style="white", justify="left")
    tabla.add_column("Cantidad", style="white", justify="center")
    tabla.add_column("Precio Unitario", style="white", justify="right")
    tabla.add_column("Subtotal", style="white", justify="right")

    for fila in detalle:
        producto = fila[7]
        categoria = fila[8]
        cantidad = fila[9]
        precio_unitario = fila[10]
        total_linea = fila[11]

        tabla.add_row(
            producto,
            categoria,
            str(cantidad),
            f"${precio_unitario:.2f}",
            f"${total_linea:.2f}"
        )

    console.print(tabla)
    console.print()
