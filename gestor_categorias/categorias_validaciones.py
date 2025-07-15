# Módulo de validaciones de categorías
# Este módulo contiene funciones para validar y gestionar las categorías,
# incluyendo la validación de nombres y la obtención de categorías eliminables.

from gestor_categorias.categorias_db import listar_categorias
from gestor_productos.productos_db import listar_productos_crudos
from core.utils import normalizar_texto
from interfaz.diseño_interfaz import mostrar_error

def obtener_categoria_por_id_validado(id_str: str):
    """
    Obtiene una categoría a partir de su ID si es válido.

    Valida que el ID ingresado sea numérico y existe en la base de datos.

    Parámetros:
        id_str (str): El ID de la categoría a validar.

    Retorna:
        tuple: La categoría correspondiente al ID si existe, None si no.
    """
    if not id_str.isdigit():
        mostrar_error("El ID debe ser un número.")
        return None

    id_categoria = int(id_str)

    # Solo intentar buscar si el ID es numérico
    encontrado = False
    for categoria in listar_categorias():
        if categoria[0] == id_categoria:
            encontrado = True
            return categoria

    if not encontrado:
        mostrar_error("El ID de categoría ingresado no existe.")
        return None

def validar_nombre_categoria(nombre: str, nombre_actual: str = None) -> bool:
    """
    Valida que el nombre de la categoría sea único y no esté vacío.
    
    (ignorando mayúsculas y tildes). Si se está editando
    una categoría, se omite la comparación con el nombre actual.

    Parámetros:
        nombre (str): El nombre de la categoría a validar.
        nombre_actual (str): El nombre actual de la categoría (si es edición).

    Retorna:
        bool: True si el nombre es válido, False si no lo es.
    """
    if not nombre:
        mostrar_error("El nombre de la categoría no puede estar vacío.")
        return False

    # Normalizar nombre para comparar sin tildes ni mayúsculas
    nombre_normalizado = normalizar_texto(nombre)
    nombres_existentes = []

    for categorias in listar_categorias():
        nombres_existentes.append(normalizar_texto(categorias[1]))

    # Si se está editando, no comparar contra el propio nombre actual
    if nombre_actual and nombre_normalizado == normalizar_texto(nombre_actual):
        return True

    if nombre_normalizado in nombres_existentes:
        mostrar_error("El nombre de la categoría ya existe.")
        return False

    return True

def listar_categorias_eliminables() -> list:
    """
    Devuelve una lista de categorías que no tienen productos asociados.

    Revisa las categorías que no tienen productos vinculados a ellas en la base de datos.

    Retorna:
        list: Lista de categorías que pueden ser eliminadas.
    """
    todas = listar_categorias()
    productos = listar_productos_crudos()

    categorias_con_productos = set()
    for producto in productos:
        if producto[2] is not None:  # producto[2] es categoria_id
            categorias_con_productos.add(producto[2])

    eliminables = []
    for categoria in todas:
        if categoria[0] not in categorias_con_productos:
            eliminables.append(categoria)

    return eliminables
