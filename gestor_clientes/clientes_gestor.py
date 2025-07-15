# Módulo de gestión de clientes
# Este módulo permite agregar, editar, eliminar y listar clientes en el sistema,
# gestionando la interacción con la base de datos y la interfaz de usuario.

from gestor_clientes.clientes_db import insertar_cliente, listar_clientes, modificar_cliente, eliminar_cliente
from interfaz.diseño_interfaz import mostrar_error, mostrar_exito, mostrar_cancelado, mostrar_info, pedir_input_con_cancelacion
from gestor_clientes.clientes_validaciones import validar_dni, obtener_cliente_por_id_validado, listar_clientes_eliminables, validar_nombre_cliente
from core.validaciones_generales import validar_telefono, validar_email
from core.utils import formatear_email, formatear_nombre
from interfaz.mostrar_resumen import mostrar_clientes
from core.logger import log_info

def agregar_cliente():
    """
    Permite agregar un nuevo cliente al sistema.

    Solicita al usuario el DNI, nombre, teléfono y correo electrónico del cliente.
    Si todos los datos son válidos, se inserta el cliente en la base de datos.
    """
    # ---- DNI ----
    while True:
        dni = pedir_input_con_cancelacion("Ingresá el DNI del cliente (C para cancelar): ")
        if dni.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if validar_dni(dni, permitir_vacio=False):
            break
    
    # ---- Nombre ----
    while True:
        nombre = pedir_input_con_cancelacion("Ingresá el nombre del nuevo cliente (C para cancelar): ")
        if nombre.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if validar_nombre_cliente(nombre, permitir_vacio=False):
            break

    # ---- Teléfono ----
    while True:
        telefono = pedir_input_con_cancelacion("Ingresá un teléfono de contacto (C para cancelar): ")
        if telefono.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if validar_telefono(telefono):
            break

    # ---- Email ----
    while True:
        email = pedir_input_con_cancelacion("Ingresá un email de contacto (C para cancelar): ")
        if email.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if validar_email(email, permitir_vacio=False):
            break

    # ---- Inserción ----
    nombre_formateado = formatear_nombre(nombre)
    email_formateado = formatear_email(email)
    if insertar_cliente(nombre_formateado, telefono, email_formateado, dni):
        mostrar_exito(f"Cliente agregado correctamente: → DNI: {dni}, Nombre: {formatear_nombre(nombre)}")
        log_info(f"Cliente agregado → DNI: {dni}, Nombre: {formatear_nombre(nombre)}")
    else:
        mostrar_error("No se pudo agregar cliente")

def editar_cliente():
    """
    Permite editar los datos de un cliente existente.

    Solicita al usuario el ID del cliente, y si es válido, permite modificar los datos
    (DNI, nombre, teléfono y email). Si se deja un campo vacío, se conserva el valor actual.
    """
    clientes = listar_clientes()
    if not clientes:
        mostrar_error("No hay clientes registrados\n")
        return

    mostrar_clientes(clientes)

    # Solicitar ID válido
    while True:
        id_cliente = pedir_input_con_cancelacion("Ingresá el ID del cliente a modificar (C para cancelar): ")
        if id_cliente.lower() == "c":
            mostrar_cancelado("Clientes")
            return

        cliente = obtener_cliente_por_id_validado(id_cliente)
        if cliente is None:  # ID ingresado no existe
            continue
        break  # ID válido

    # Datos actuales
    nombre_actual = cliente[1]
    telefono_actual = cliente[2]
    email_actual = cliente[3]
    dni_actual = cliente[4]

    # --- DNI ---
    while True:
        mostrar_info(f"DNI actual: {dni_actual}")
        nuevo_dni = pedir_input_con_cancelacion("Ingresá el nuevo DNI (Enter para dejar igual, C para cancelar): ")
        if nuevo_dni.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if not nuevo_dni:
            nuevo_dni = dni_actual
            break
        if validar_dni(nuevo_dni, dni_actual=dni_actual, permitir_vacio=True):
            break

    # --- Nombre ---
    while True:
        mostrar_info(f"Nombre actual: {nombre_actual}")
        nuevo_nombre = pedir_input_con_cancelacion("Ingresá el nuevo nombre (Enter para dejar igual, C para cancelar): ")
        if nuevo_nombre.lower() == "c":
            mostrar_cancelado("Clientes")
            return
        if not nuevo_nombre:
            nuevo_nombre = nombre_actual
        if validar_nombre_cliente(nuevo_nombre, permitir_vacio=True):
            break

    # --- Teléfono ---
    while True:
        mostrar_info(f"Teléfono actual: {telefono_actual}")
        nuevo_telefono = pedir_input_con_cancelacion("Ingresá el nuevo teléfono (Enter para dejar igual, C para cancelar): ")
        if nuevo_telefono.lower() == "c":
            mostrar_cancelado("Clientes")
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
            mostrar_cancelado("Clientes")
            return
        if not nuevo_email:
            nuevo_email = email_actual
        if validar_email(nuevo_email, permitir_vacio=True):
            break

    # --- Actualización ---
    if modificar_cliente(
        id_cliente,
        formatear_nombre(nuevo_nombre),
        nuevo_telefono,
        formatear_email(nuevo_email),
        nuevo_dni
    ):
        mostrar_exito(f"Cliente editado correctamente → ID: {id_cliente}")
        log_info(f"Cliente editado → ID: {id_cliente}")
    else:
        mostrar_error("No se pudo modificar cliente")


def borrar_cliente():
    """
    Permite eliminar un cliente del sistema.

    Solicita el ID de un cliente, valida si el cliente tiene facturas asociadas y, si no,
    elimina el cliente de la base de datos.
    """
    clientes = listar_clientes()
    clientes_eliminables = listar_clientes_eliminables()
    if not clientes:
        mostrar_error("No hay clientes registrados\n")
        return
    if clientes and not clientes_eliminables:
        mostrar_error("No hay clientes que puedan ser eliminados (todos tienen facturas asociadas)\n")
        return

    mostrar_clientes(clientes_eliminables)

    mostrar_info("Solo se muestran los clientes que **no tienen facturas asociadas** y pueden ser eliminados")

    while True:
        id_cliente = pedir_input_con_cancelacion("Ingresá el ID del cliente a eliminar (C para cancelar): ")
        if id_cliente.lower() == "c":
            mostrar_cancelado("Clientes")
            return

        cliente = obtener_cliente_por_id_validado(id_cliente)
        if cliente is None:  # ID ingresado no existe
            continue
        if cliente not in clientes_eliminables:
            mostrar_error("El ID ingresado no corresponde a un cliente eliminable")
            continue
        break  # ID válido

    if eliminar_cliente(id_cliente):
        mostrar_exito(f"Cliente eliminado correctamente → ID: {id_cliente}")
        log_info(f"Cliente eliminado → ID: {id_cliente}")
    else:
        mostrar_error("No se pudo eliminar el cliente")


def mostrar_todos_los_clientes():
    """
    Muestra todos los clientes registrados en el sistema.

    Si no existen clientes, muestra un mensaje de error.
    """
    clientes = listar_clientes()
    if clientes:
        mostrar_clientes(clientes)
    else:
        mostrar_error("No hay clientes registrados\n")
