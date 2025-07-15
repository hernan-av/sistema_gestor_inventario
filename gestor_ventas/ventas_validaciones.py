# Módulo de validaciones y utilidades para ventas
# Este módulo contiene funciones de validación relacionadas con las ventas, como la carga de productos a la venta
# y la validación del stock y cantidad disponible.

from gestor_productos.productos_db import listar_productos
from interfaz.mostrar_resumen import mostrar_productos
from interfaz.diseño_interfaz import mostrar_error, mostrar_cancelado, mostrar_info
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from gestor_productos.productos_validaciones import obtener_producto_por_id_validado

def cargar_productos_para_venta() -> list[dict] | str:
    """
    Permite cargar uno o más productos a una venta, validando stock y cantidad.
    
    Esta función pide al usuario que ingrese el ID del producto y la cantidad a vender, y valida que la cantidad
    no sea mayor que el stock disponible. Si el usuario decide cancelar, la función devuelve "CANCELADO". 
    Si no se ingresan productos válidos, también se devuelve "CANCELADO".

    Retorna:
        list[dict]: Lista de diccionarios con los productos y cantidades seleccionados para la venta.
        str: "CANCELADO" si el usuario cancela la operación o si no se cargan productos válidos.
    """
    productos_disponibles = listar_productos()
    if not productos_disponibles:
        mostrar_error("No hay productos cargados en el sistema.")
        return "CANCELADO"

    mostrar_productos(productos_disponibles)
    productos = []

    mostrar_info("Si el producto no existe, primero crealo y luego reintenta la venta")

    while True:
        id_producto = pedir_input_con_cancelacion("Ingresá el ID del producto que querés vender (C para cancelar): ")
        if id_producto.lower() == "c":
            mostrar_cancelado("Ventas")
            return "CANCELADO"

        producto_elegido = obtener_producto_por_id_validado(id_producto)
        if producto_elegido is None:
            continue

        nombre, stock_disponible, precio_unitario = producto_elegido[1], producto_elegido[4], producto_elegido[5]

        while True:
            mostrar_info(f"Stock disponible: {stock_disponible} unidades | Precio unitario: ${precio_unitario:.2f}")
            cantidad_input = pedir_input_con_cancelacion(f"Ingresá la cantidad a vender de '{nombre}' (C para cancelar): ")
            if cantidad_input.lower() == "c":
                mostrar_cancelado("Ventas")
                return "CANCELADO"

            if not cantidad_input.isdigit():
                mostrar_error("La cantidad debe ser un número entero.")
                continue

            cantidad = int(cantidad_input)
            if cantidad <= 0 or cantidad > stock_disponible:
                mostrar_error("Cantidad inválida o supera el stock disponible.")
                continue
            break

        productos.append({
                "producto_id": producto_elegido[0],
                "cantidad": cantidad
            })

        continuar = pedir_input_con_cancelacion("¿Querés agregar otro producto? (S para seguir agregando / cualquier otra letra para finalizar): ")
        if continuar.lower() != "s":
            break

    return productos if productos else "CANCELADO"
