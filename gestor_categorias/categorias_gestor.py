# Módulo de gestión de categorías
# Este módulo permite agregar, editar, eliminar y listar categorías, así como gestionar 
# la base de datos y la interacción con la interfaz para la gestión de categorías.

from gestor_categorias.categorias_db import insertar_categoria, listar_categorias, modificar_categoria, eliminar_categoria
from gestor_categorias.categorias_validaciones import obtener_categoria_por_id_validado, validar_nombre_categoria, listar_categorias_eliminables
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from interfaz.mostrar_resumen import mostrar_categorias
from interfaz.diseño_interfaz import mostrar_error, mostrar_exito, mostrar_cancelado, mostrar_info
from core.utils import formatear_nombre
from core.validaciones_generales import validar_nombre
from core.logger import log_info

def agregar_categoria() -> None:
    """
    Permite agregar una nueva categoría a la base de datos.

    Solicita al usuario el nombre de la categoría y verifica que sea válido.
    Si es válido, se agrega la categoría a la base de datos.
    """
    while True:
        nombre = pedir_input_con_cancelacion("Ingresá el nombre de la nueva categoría (C para cancelar): ")
        if nombre.lower() == "c":
            mostrar_cancelado("Categorías")
            return
        if not validar_nombre_categoria(nombre):
            continue
        break  # Nombre válido y único

    nombre_formateado = formatear_nombre(nombre)
    if insertar_categoria(nombre_formateado):
        mostrar_exito(f"Categoría agregada correctamente → {nombre_formateado}")
        log_info(f"Categoría agregada → {nombre_formateado}")
    else:
        mostrar_error("No se pudo agregar la categoría.")

def editar_categoria() -> None:
    """
    Permite editar el nombre de una categoría existente.

    Solicita al usuario el ID de la categoría a editar, verifica su existencia,
    y luego permite modificar su nombre si se cumplen las validaciones.
    """
    categorias = listar_categorias()
    if not categorias:
        mostrar_error("No hay categorías registradas\n")
        return

    mostrar_categorias(categorias)

    while True:
        id_categoria = pedir_input_con_cancelacion("Ingresá el ID de la categoría a editar (C para cancelar): ")
        if id_categoria.lower() == "c":
            mostrar_cancelado("Categorías")
            return

        categoria = obtener_categoria_por_id_validado(id_categoria)
        if categoria is None:  # ID ingresado no existe
            continue
        break  # ID válido

    while True:
        nuevo_nombre = pedir_input_con_cancelacion("Ingresá el nuevo nombre de la categoría (C para cancelar): ")
        if nuevo_nombre.lower() == "c":
            mostrar_cancelado("Categorías")
            return
        if not validar_nombre(nuevo_nombre):
            continue
        if not validar_nombre_categoria(nuevo_nombre):
            continue
        break  # Nombre válido y único

    nombre_formateado = formatear_nombre(nuevo_nombre)
    if modificar_categoria(id_categoria, nombre_formateado):
        mostrar_exito(f"Categoría editada correctamente → ID: {id_categoria}, Nuevo nombre: {nombre_formateado}")
        log_info(f"Categoría editada → ID: {id_categoria}, Nuevo nombre: {nombre_formateado}")
    else:
        mostrar_error("No se pudo modificar la categoría.")

def borrar_categoria() -> None:
    """
    Permite eliminar una categoría que no tenga productos asociados.

    Solicita al usuario el ID de la categoría a eliminar, verifica que sea eliminable
    y la elimina de la base de datos si se cumplen las condiciones.
    """
    categorias = listar_categorias()
    categorias_eliminables = listar_categorias_eliminables()
    if not categorias:
        mostrar_error("No hay categorías registradas\n")
        return        
    if categorias and not categorias_eliminables:
        mostrar_error("No hay categorías que puedan ser eliminadas (todas tienen productos asociados)\n")
        return

    mostrar_categorias(categorias_eliminables)

    mostrar_info("Solo se muestran las categorías que **no tienen productos asociados** y pueden ser eliminadas.")

    while True:
        id_categoria = pedir_input_con_cancelacion("Ingresá el ID de la categoría a eliminar (C para cancelar): ")
        if id_categoria.lower() == "c":
            mostrar_cancelado("Categorías")
            return

        categoria = obtener_categoria_por_id_validado(id_categoria)
        if categoria is None:  # ID ingresado no existe
            continue
        if categoria not in categorias_eliminables:
            mostrar_error("El ID ingresado no corresponde a una categoría eliminable")
            continue
        break  # ID válido

    if eliminar_categoria(id_categoria):
        mostrar_exito(f"Categoría eliminada correctamente → ID: {id_categoria}")
        log_info(f"Categoría eliminada → ID: {id_categoria}")
    else:
        mostrar_error("No se pudo eliminar la categoría")

def mostrar_todas_las_categorias() -> None:
    """
    Muestra todas las categorías registradas en el sistema.

    Si no existen categorías, muestra un mensaje de error.
    """
    categorias = listar_categorias()
    if categorias:
        mostrar_categorias(categorias)
    else:
        mostrar_error("No hay categorías registradas\n")
