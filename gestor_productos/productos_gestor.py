# Módulo de gestión de productos
# Este módulo permite agregar, editar, eliminar y listar productos en el sistema,
# gestionando la interacción con la base de datos y la interfaz de usuario.

from gestor_productos.productos_db import insertar_producto, listar_productos, modificar_producto, eliminar_producto
from gestor_productos.productos_validaciones import validar_precio, validar_stock, obtener_producto_por_id_validado
from gestor_categorias.categorias_db import listar_categorias
from gestor_categorias.categorias_validaciones import obtener_categoria_por_id_validado
from gestor_proveedores.proveedores_db import listar_proveedores
from gestor_proveedores.proveedores_validaciones import obtener_proveedor_por_id_validado
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from interfaz.diseño_interfaz import mostrar_error, mostrar_exito, mostrar_cancelado, mostrar_info
from interfaz.mostrar_resumen import mostrar_productos, mostrar_categorias, mostrar_proveedores
from core.utils import formatear_nombre
from core.logger import log_info
from core.validaciones_generales import validar_nombre

def agregar_producto():
    """
    Permite agregar un nuevo producto al sistema.

    Solicita al usuario el nombre, categoría, proveedor, stock y precio del producto.
    Si todos los datos son válidos, se inserta el producto en la base de datos.
    """
    # ---- Nombre ----
    while True:
        nombre = pedir_input_con_cancelacion("Ingresá el nombre del nuevo producto (C para cancelar): ")
        if nombre.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if validar_nombre(nombre):
            break

    # ---- Categoría ----
    categorias = listar_categorias()
    if not categorias:
        mostrar_error("No hay categorías registradas. Creá una antes de continuar.")
        return
    mostrar_categorias(categorias)

    while True:
        id_categoria = pedir_input_con_cancelacion("Ingresá el ID de la categoría (C para cancelar): ")
        if id_categoria.lower() == "c":
            mostrar_cancelado("Productos")
            return
        
        categoria = obtener_categoria_por_id_validado(id_categoria)
        if categoria is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # ---- Proveedor ----
    proveedores = listar_proveedores()
    if not proveedores:
        mostrar_error("No hay proveedores registrados. Creá uno antes de continuar.")
        return
    mostrar_proveedores(proveedores)

    while True:
        id_proveedor = pedir_input_con_cancelacion("Ingresá el ID del proveedor (C para cancelar): ")
        if id_proveedor.lower() == "c":
            mostrar_cancelado("Productos")
            return
        proveedor = obtener_proveedor_por_id_validado(id_proveedor)
        if proveedor is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # ---- Stock ----
    while True:
        stock_cantidad = pedir_input_con_cancelacion("Ingresá el stock a cargar (C para cancelar): ")
        if stock_cantidad.lower() == "c":
            mostrar_cancelado("Productos")
            return

        stock = validar_stock(stock_cantidad)
        if stock is None:  # Sin stock
            continue
        break  # Stock ok

    # ---- Precio unitario ----
    while True:
        precio_unitario = pedir_input_con_cancelacion("Ingresá el precio unitario (C para cancelar): ")
        if precio_unitario.lower() == "c":
            mostrar_cancelado("Productos")
            return

        precio = validar_precio(precio_unitario)
        if precio is None:
            continue
        break

    # ---- Inserción ----
    nombre_formateado = formatear_nombre(nombre)
    if insertar_producto(nombre_formateado, id_categoria, id_proveedor, stock, precio):
        mostrar_exito(f"Producto agregado correctamente → Nombre: {nombre_formateado}")
        log_info(f"Producto agregado → Nombre: {nombre_formateado}")
    else:
        mostrar_error("No se pudo agregar el producto.")

def editar_producto():
    """
    Permite editar los datos de un producto existente.

    Solicita al usuario el ID del producto y, si es válido, permite modificar los datos
    (nombre, categoría, proveedor, stock y precio). Si se deja un campo vacío, se conserva el valor actual.
    """
    productos = listar_productos()
    if not productos:
        mostrar_error("No hay productos registrados\n")
        return

    mostrar_productos(productos)

    # --- Solicitar ID válido ---
    while True:
        id_producto = pedir_input_con_cancelacion("Ingresá el ID del producto a modificar (C para cancelar): ")
        if id_producto.lower() == "c":
            mostrar_cancelado("Productos")
            return

        producto = obtener_producto_por_id_validado(id_producto)
        if producto is None:  # ID ingresado no existe
            continue
        break  # ID válido

    nombre_actual = producto[1]
    id_categoria_actual = producto[2]
    id_proveedor_actual = producto[3]
    stock_actual = producto[4]
    precio_actual = producto[5]

    # --- Nombre ---
    while True:
        mostrar_info(f"Nombre actual: {nombre_actual}")
        nuevo_nombre = pedir_input_con_cancelacion("Ingresá el nuevo nombre (Enter para dejar igual, C para cancelar): ")
        if nuevo_nombre.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if not nuevo_nombre:
            nuevo_nombre = nombre_actual
        if validar_nombre(nuevo_nombre):
            break

    # --- Categoría ---
    categorias = listar_categorias()
    if not categorias:
        mostrar_error("No hay categorías disponibles.")
        return
    mostrar_categorias(categorias)

    while True:
        mostrar_info(f"Categoría actual: {id_categoria_actual}")
        nueva_categoria = pedir_input_con_cancelacion("Ingresá el ID de la nueva categoría (Enter para dejar igual, C para cancelar): ")
        if nueva_categoria.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if not nueva_categoria:
            nueva_categoria = id_categoria_actual
            break
        categoria = obtener_categoria_por_id_validado(nueva_categoria)
        if categoria is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # --- Proveedor ---
    proveedores = listar_proveedores()
    if not proveedores:
        mostrar_error("No hay proveedores registrados.")
        return
    mostrar_proveedores(proveedores)

    while True:
        mostrar_info(f"Proveedor actual: {id_proveedor_actual}")
        nuevo_proveedor = pedir_input_con_cancelacion("Ingresá el ID del nuevo proveedor (Enter para dejar igual, C para cancelar): ")
        if nuevo_proveedor.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if not nuevo_proveedor:
            nuevo_proveedor = id_proveedor_actual
            break
        proveedor = obtener_proveedor_por_id_validado(nuevo_proveedor)
        if proveedor is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # --- Stock ---
    while True:
        mostrar_info(f"Stock actual: {stock_actual}")
        nuevo_stock = pedir_input_con_cancelacion("Ingresá el nuevo stock (Enter para dejar igual, C para cancelar): ")
        if nuevo_stock.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if not nuevo_stock:  # Si se deja vacío, mantener valor actual
            stock = stock_actual
            break
        stock = validar_stock(nuevo_stock)
        if stock is not None:
            break

    # --- Precio ---
    while True:
        mostrar_info(f"Precio actual: ${precio_actual:.2f}")
        nuevo_precio = pedir_input_con_cancelacion("Ingresá el nuevo precio unitario (Enter para dejar igual, C para cancelar): ")
        if nuevo_precio.lower() == "c":
            mostrar_cancelado("Productos")
            return
        if not nuevo_precio:
            precio = precio_actual
            break
        precio = validar_precio(nuevo_precio)
        if precio is not None:
            break

    # --- Actualización ---
    nombre_formateado = formatear_nombre(nuevo_nombre)
    id_categoria_final = nueva_categoria
    id_proveedor_final = nuevo_proveedor

    if modificar_producto(
        id_producto,
        nombre_formateado,
        id_categoria_final,
        id_proveedor_final,
        stock,
        precio
    ):
        mostrar_exito(f"Producto editado correctamente → ID: {id_producto}")
        log_info(f"Producto editado → ID: {id_producto}")
    else:
        mostrar_error("No se pudo modificar el producto.")


def borrar_producto():
    """
    Permite eliminar un producto del sistema.

    Solicita el ID de un producto, valida si el producto existe y lo elimina de la base de datos.
    """
    productos = listar_productos()
    if not productos:
        mostrar_error("No hay productos registrados\n")
        return

    mostrar_productos(productos)

    while True:
        id_producto = pedir_input_con_cancelacion("Ingresá el ID del producto a eliminar (C para cancelar): ")
        if id_producto.lower() == "c":
            mostrar_cancelado("Productos")
            return

        producto = obtener_proveedor_por_id_validado(id_producto)
        if producto is None:  # ID ingresado no existe
            continue
        break  # ID válido

    if eliminar_producto(id_producto):
        mostrar_exito(f"Producto eliminado correctamente → ID: {id_producto}")
        log_info(f"Producto eliminado → ID: {id_producto}")
    else:
        mostrar_error("No se pudo eliminar el producto.")

def mostrar_todos_los_productos():
    """
    Muestra todos los productos registrados en el sistema.

    Si no existen productos, muestra un mensaje de error.
    """
    productos = listar_productos()
    if productos:
        mostrar_productos(productos)
    else:
        mostrar_error("No hay productos registrados\n")
