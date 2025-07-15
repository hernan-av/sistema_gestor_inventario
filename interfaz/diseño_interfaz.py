# Módulo Rich para consola y texto estilizado

from rich.console import Console
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel

# ======================= COLORES =======================
COLOR_TITULO = "bold bright_green"
COLOR_NUMERO = "bold bright_green"
COLOR_TEXTO = "bold bright_green"
COLOR_INPUT = "bold bright_green"
COLOR_ERROR = "bold bright_red"
COLOR_EXITO = "medium_turquoise"
COLOR_INFO = "bright_yellow"
COLOR_SEPARADOR = "bold bright_green"

console = Console()

# ======================= ENCABEZADOS =======================
def encabezado_seccion(nombre: str):
    """
    Muestra un encabezado con el nombre de la sección.

    Args:
        nombre (str): El nombre de la sección.
    """
    console.print()
    console.print(Rule(Text(nombre, style=COLOR_TITULO), style=COLOR_SEPARADOR))

# ======================= MENSAJES =======================
def mostrar_bienvenida():
    """Muestra un mensaje de bienvenida y carga inicial."""
    console.clear()

    titulo = Text("Electro Mundo S.A.", style=COLOR_TITULO, justify="center")
    panel = Panel(titulo, border_style=COLOR_SEPARADOR, expand=True)
    console.print(panel)

    console.print(Rule(Text(">>> Sistema de Gestión de Inventario v1.0 <<<", style=COLOR_TITULO), style=COLOR_SEPARADOR))
    console.print(f"[{COLOR_TEXTO}]Inicializando módulos...[/]")
    console.print(f"[{COLOR_TEXTO}]Cargando base de datos...[/]")
    console.print(f"[{COLOR_TEXTO}]Componentes verificados.[/]")
    console.print(f"[{COLOR_TEXTO}]Presione Enter para continuar ▋[/]")

    while True:
        entrada = input()
        if entrada == "":
            break
        console.print(f"[bold bright_green]Error ▌ Entrada no válida — presione solo Enter para continuar[/bold bright_green]")

def mostrar_error(texto: str):
    """
    Muestra un mensaje de error en la consola.

    Args:
        texto (str): El mensaje de error.
    """
    texto = str(texto)
    console.print(f"\n[{COLOR_ERROR}]▌ {texto}[/{COLOR_ERROR}]")

def mostrar_exito(texto: str):
    """
    Muestra un mensaje de éxito en la consola.

    Args:
        texto (str): El mensaje de éxito.
    """
    texto = str(texto)
    console.print(f"\n[{COLOR_EXITO}]▌ {texto}[/{COLOR_EXITO}]\n")

def mostrar_info(texto: str):
    """
    Muestra un mensaje informativo en la consola.

    Args:
        texto (str): El mensaje informativo.
    """
    texto = str(texto)
    console.print(f"\n[{COLOR_INFO}]▌ {texto}[/{COLOR_INFO}]")

def mostrar_cancelado(seccion: str):
    """
    Muestra un mensaje indicando que la acción fue cancelada y se vuelve al menú.

    Args:
        seccion (str): El nombre de la sección en la que se estaba.
    """
    console.print(f"\n[{COLOR_INFO}]▌↩ Acción cancelada. Volviendo al menú de [bold]{seccion}[/bold][{COLOR_INFO}].\n")

def pedir_input_con_cancelacion(prompt: str) -> str:
    """
    Pide una entrada al usuario con la opción de cancelar (ingresando 'C').

    Args:
        prompt (str): El mensaje a mostrar al usuario.

    Retorna:
        str: La entrada del usuario o 'c' si canceló.
    """
    console.print(f"\n[{COLOR_INPUT}]{prompt}[/{COLOR_INPUT}]", end="")
    entrada = input().strip()
    if entrada.lower() == "c":
        return "c"
    return entrada

# ======================= MENÚS =======================
def mostrar_menu_principal() -> str:
    """
    Muestra el menú principal de la aplicación.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(mostrar_menu_principal, "_encabezado_mostrado") or not mostrar_menu_principal._encabezado_mostrado:
        encabezado_seccion("Menú Principal")
        mostrar_menu_principal._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ventas[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Clientes[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Proveedores[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]4[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Productos[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]5[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Categorías[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Salir[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()

def menu_ventas() -> str:
    """
    Muestra el menú de ventas.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(menu_ventas, "_encabezado_mostrado") or not menu_ventas._encabezado_mostrado:
        encabezado_seccion("Ventas")
        menu_ventas._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Registrar venta[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ver todas las facturas[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Exportar factura por ID[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Volver al menú principal[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()

def menu_clientes() -> str:
    """
    Muestra el menú de clientes.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(menu_clientes, "_encabezado_mostrado") or not menu_clientes._encabezado_mostrado:
        encabezado_seccion("Clientes")
        menu_clientes._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Agregar cliente[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ver todos los clientes[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Editar cliente[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]4[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Eliminar cliente[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Volver[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()

def menu_proveedores() -> str:
    """
    Muestra el menú de proveedores.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(menu_proveedores, "_encabezado_mostrado") or not menu_proveedores._encabezado_mostrado:
        encabezado_seccion("Proveedores")
        menu_proveedores._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Agregar proveedor[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ver todos los proveedores[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Editar proveedor[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]4[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Eliminar proveedor[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Volver[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()

def menu_productos() -> str:
    """
    Muestra el menú de productos.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(menu_productos, "_encabezado_mostrado") or not menu_productos._encabezado_mostrado:
        encabezado_seccion("Productos")
        menu_productos._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Agregar producto[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ver todos los productos[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Editar producto[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]4[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Eliminar producto[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Volver[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()

def menu_categorias() -> str:
    """
    Muestra el menú de categorías.

    Retorna:
        str: La opción seleccionada por el usuario.
    """
    if not hasattr(menu_categorias, "_encabezado_mostrado") or not menu_categorias._encabezado_mostrado:
        encabezado_seccion("Categorías")
        menu_categorias._encabezado_mostrado = True

    console.print(f"[{COLOR_NUMERO}]1[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Agregar categoría[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]2[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Ver categorías[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]3[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Editar categoría[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]4[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Eliminar categoría[/{COLOR_TEXTO}]")
    console.print(f"[{COLOR_NUMERO}]0[/{COLOR_NUMERO}]. [{COLOR_TEXTO}]Volver[/{COLOR_TEXTO}]")
    return console.input(f"\n[{COLOR_INPUT}]Seleccioná una opción:[/{COLOR_INPUT}] ").strip()
