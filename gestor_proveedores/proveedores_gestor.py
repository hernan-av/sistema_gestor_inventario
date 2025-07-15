# Módulo de gestión de proveedores
# Este módulo maneja las operaciones de gestión de proveedores en el sistema,
# permitiendo agregar, editar, eliminar y listar proveedores.

from gestor_proveedores.proveedores_db import insertar_proveedor, listar_proveedores, modificar_proveedor, eliminar_proveedor
from interfaz.diseño_interfaz import mostrar_error, mostrar_exito, mostrar_cancelado, mostrar_info
from gestor_proveedores.proveedores_validaciones import validar_cuit, obtener_proveedor_por_id_validado, listar_proveedores_eliminables, proveedor_tiene_productos
from core.validaciones_generales import validar_nombre, validar_telefono, validar_email
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from interfaz.mostrar_resumen import mostrar_proveedores
from core.utils import formatear_nombre, formatear_email
from core.logger import log_info

def agregar_proveedor():
    """
    Permite agregar un nuevo proveedor al sistema.

    Solicita al usuario el CUIT, nombre, teléfono, y email del proveedor.
    Si todos los datos son válidos, se inserta el proveedor en la base de datos.
    """
    # ---- CUIT ----
    while True:
        cuit = pedir_input_con_cancelacion("Ingresá el CUIT del proveedor (C para cancelar): ")
        if cuit.lower() == "c":
            mostrar_cancelado("Proveedores")
            return
        if validar_cuit(cuit, permitir_vacio=False):
            break
    
    # ---- Nombre ----
    while True:
        nombre = pedir_input_con_cancelacion("Ingresá el nombre del nuevo proveedor (C para cancelar): ")
        if nombre.lower() == 'c':
            mostrar_cancelado("Proveedores")
            return
        if validar_nombre(nombre, permitir_vacio=False):
            break

    # ---- Teléfono ----
    while True:
        telefono = pedir_input_con_cancelacion("Ingresá un teléfono de contacto (C para cancelar): ")
        if telefono == 'c':
            mostrar_cancelado("Proveedores")
            return
        if validar_telefono(telefono, permitir_vacio=False):
            break

    # ---- Email ----
    while True:
        email = pedir_input_con_cancelacion("Ingresá un email de contacto (C para cancelar): ")
        if email.lower() == "c":
            mostrar_cancelado("Proveedores")
            return
        if validar_email(email, permitir_vacio=False):
            break

    # ---- Inserción ----
    nombre_formateado = formatear_nombre(nombre)
    email_formateado = formatear_email(email)
    if insertar_proveedor(nombre_formateado, telefono, email_formateado, cuit):
        mostrar_exito(f"Proveedor agregado correctamente → CUIT: {cuit}, Nombre: {formatear_nombre(nombre)}")
        log_info(f"Proveedor agregado → CUIT: {cuit}, Nombre: {formatear_nombre(nombre)}")
    else:
        mostrar_error("No se pudo agregar proveedor")

def editar_proveedor():
    """
    Permite editar los datos de un proveedor existente.

    Solicita al usuario el ID del proveedor y, si es válido, permite modificar los datos
    (CUIT, nombre, teléfono, y email). Si se deja un campo vacío, se conserva el valor actual.
    """
    proveedores = listar_proveedores()
    if not proveedores:
        mostrar_error("No hay proveedores registrados\n")
        return

    mostrar_proveedores(proveedores)

    # --- Solicitar ID válido ---
    while True:
        id_proveedor = pedir_input_con_cancelacion("Ingresá el ID del proveedor a modificar (C para cancelar): ")
        if id_proveedor.lower() == "c":
            mostrar_cancelado("Proveedores")
            return

        proveedor = obtener_proveedor_por_id_validado(id_proveedor)
        if proveedor is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # --- Guardar valores actuales ---
    nombre_actual = proveedor[1]
    telefono_actual = proveedor[2]
    email_actual = proveedor[3]
    cuit_actual = proveedor[4]

    # --- CUIT ---
    tiene_productos = proveedor_tiene_productos(id_proveedor)
    if tiene_productos:
        mostrar_info("Este proveedor tiene productos asociados. No se puede modificar el CUIT.")
        nuevo_cuit = cuit_actual
    else:
        while True:
            mostrar_info(f"CUIT actual: {cuit_actual}")
            nuevo_cuit = pedir_input_con_cancelacion("Ingresá el nuevo CUIT (Enter para dejar igual, C para cancelar): ")
            if nuevo_cuit.lower() == "c":
                mostrar_cancelado("Proveedores")
                return
            if not nuevo_cuit:
                nuevo_cuit = cuit_actual
                break
            if validar_cuit(nuevo_cuit, cuit_actual=cuit_actual, permitir_vacio=True):
                break

    # --- Nombre ---
    while True:
        mostrar_info(f"Nombre actual: {nombre_actual}")
        nuevo_nombre = pedir_input_con_cancelacion("Ingresá el nuevo nombre (Enter para dejar igual, C para cancelar): ")
        if nuevo_nombre.lower() == "c":
            mostrar_cancelado("Proveedores")
            return
        if not nuevo_nombre:
            nuevo_nombre = nombre_actual
        if validar_nombre(nuevo_nombre, permitir_vacio=True):
            break

    # --- Teléfono ---
    while True:
        mostrar_info(f"Teléfono actual: {telefono_actual}")
        nuevo_telefono = pedir_input_con_cancelacion("Ingresá el nuevo teléfono (Enter para dejar igual, C para cancelar): ")
        if nuevo_telefono.lower() == "c":
            mostrar_cancelado("Proveedores")
            return
        if not nuevo_telefono:
            nuevo_telefono = telefono_actual
            break
        if validar_telefono(nuevo_telefono, permitir_vacio=True):
            break

    # --- Email ---
    while True:
        mostrar_info(f"Email actual: {email_actual}")
        nuevo_email = pedir_input_con_cancelacion("Ingresá el nuevo email (Enter para dejar igual, C para cancelar): ")
        if nuevo_email.lower() == "c":
            mostrar_cancelado("Proveedores")
            return
        if not nuevo_email:
            nuevo_email = email_actual
        if validar_email(nuevo_email, permitir_vacio=True):
            break

    if modificar_proveedor(
        id_proveedor,
        formatear_nombre(nuevo_nombre),
        nuevo_telefono,
        formatear_email(nuevo_email),
        nuevo_cuit
    ):
        mostrar_exito(f"Proveedor editado correctamente → ID {id_proveedor}")
        log_info(f"Proveedor editado → ID {id_proveedor}")
    else:
        mostrar_error("No se pudo editar proveedor")

def borrar_proveedor():
    """
    Permite eliminar un proveedor del sistema.

    Solicita el ID de un proveedor, valida si el proveedor tiene productos asociados y,
    si no, elimina el proveedor de la base de datos.
    """
    proveedores = listar_proveedores()
    proveedores_eliminables = listar_proveedores_eliminables()
    if not proveedores:
        mostrar_error("No hay proveedores registrados\n")
        return
    if proveedores and not proveedores_eliminables:
        mostrar_error("No hay proveedores que puedan ser eliminados (todos tienen productos asociados)\n")
        return

    mostrar_proveedores(proveedores_eliminables)

    mostrar_info("Solo se muestran los proveedores que **no tienen productos asociados** y pueden ser eliminados.")

    while True:
        id_proveedor = pedir_input_con_cancelacion("Ingresá el ID del proveedor a eliminar (C para cancelar): ")
        if id_proveedor.lower() == "c":
            mostrar_cancelado("Proveedores")
            return

        proveedor = obtener_proveedor_por_id_validado(id_proveedor)
        if proveedor is None:  # ID proveedor no existe
            continue
        if proveedor not in proveedores_eliminables:
            mostrar_error("El ID ingresado no corresponde a un proveedor eliminable.")
            continue
        break  # ID válido

    if eliminar_proveedor(id_proveedor):
        mostrar_exito(f"Proveedor eliminado correctamente → ID: {id_proveedor}")
        log_info(f"Proveedor eliminado → ID: {id_proveedor}")
    else:
        mostrar_error("No se pudo eliminar el proveedor.")

def mostrar_todos_los_proveedores():
    """
    Muestra todos los proveedores registrados en el sistema.

    Si no existen proveedores, muestra un mensaje de error.
    """
    proveedores = listar_proveedores()
    if proveedores:
        mostrar_proveedores(proveedores)
    else:
        mostrar_error("No hay proveedores registrados\n")
