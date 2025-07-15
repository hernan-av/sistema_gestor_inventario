# Módulo de gestión de exportación de facturas
# Este módulo permite generar un archivo PDF con la información de una factura y exportarla,
# así como gestionar la exportación de facturas desde la base de datos.

from fpdf import FPDF
from datetime import datetime
import os

from gestor_ventas.facturas_db import obtener_detalle_venta, listar_facturas
from interfaz.mostrar_resumen import mostrar_facturas
from interfaz.diseño_interfaz import pedir_input_con_cancelacion
from interfaz.diseño_interfaz import mostrar_error, mostrar_cancelado, mostrar_exito
from core.logger import log_info, log_error

RUTA_FACTURAS = "./facturas_exportadas"

def generar_pdf_factura(id_factura: int) -> str | None:
    """
    Genera un archivo PDF con los detalles de una factura.

    Extrae la información de la factura y sus productos asociados desde la base de datos,
    luego genera un archivo PDF con el formato adecuado.

    Parámetros:
        id_factura (int): El ID de la factura que se quiere exportar a PDF.

    Retorna:
        str: La ruta del archivo PDF generado si la operación fue exitosa, None en caso de error.
    """
    detalle = obtener_detalle_venta(id_factura)
    if not detalle:
        log_error(f"No se encontró información para la factura ID {id_factura}")
        return None

    try:
        (
            _, fecha, cliente_id, nombre_cliente, email, dni,
            _, producto, categoria, cantidad, precio_unitario, total_linea, total_factura
        ) = detalle[0]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # ENCABEZADO EMPRESA
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(190, 10, "Electro Mundo S.A.", ln=True, align="C")
        pdf.set_font("Arial", size=10)
        pdf.cell(190, 6, "CUIT: 30-12345678-9 | contacto@gestionavanzada.com", ln=True, align="C")
        pdf.cell(190, 6, "Av. Siempre Viva 123, CABA | Tel: (011) 4567-8910", ln=True, align="C")
        pdf.ln(4)

        # DATOS FACTURA
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(190, 10, f"FACTURA Nº {id_factura}", ln=True, align="C")
        pdf.set_font("Arial", size=11)
        pdf.cell(190, 8, f"Fecha: {fecha}", ln=True)
        pdf.cell(190, 8, f"Cliente: {nombre_cliente} (ID: {cliente_id})", ln=True)
        pdf.cell(190, 8, f"Email: {email}", ln=True)
        pdf.cell(190, 8, f"DNI: {dni}", ln=True)

        # TABLA PRODUCTOS
        pdf.ln(5)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 8, "Detalle de Productos", ln=True)
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(50, 8, "Producto", border=1, fill=1)
        pdf.cell(40, 8, "Categoría", border=1, fill=1)
        pdf.cell(25, 8, "Cantidad", border=1, fill=1, align="C")
        pdf.cell(35, 8, "Precio Unit.", border=1, fill=1, align="R")
        pdf.cell(40, 8, "Subtotal", border=1, ln=True, fill=1, align="R")

        pdf.set_font("Arial", size=10)
        for row in detalle:
            (_, _, _, _, _, _, _, producto, categoria,
            cantidad, precio_unitario, total_linea, _) = row

            pdf.cell(50, 8, producto, border=1)
            pdf.cell(40, 8, categoria, border=1)
            pdf.cell(25, 8, str(cantidad), border=1, align="C")
            pdf.cell(35, 8, f"${precio_unitario:.2f}", border=1, align="R")
            pdf.cell(40, 8, f"${total_linea:.2f}", border=1, ln=True, align="R")

        pdf.ln(4)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(150, 8, "TOTAL FACTURA:", align="R")
        pdf.set_font("Arial", style="", size=12)
        pdf.cell(40, 8, f"${total_factura:.2f}", ln=True, align="R")

        # GUARDADO
        os.makedirs(RUTA_FACTURAS, exist_ok=True)
        nombre_archivo = f"factura_{id_factura}_{timestamp}.pdf"
        ruta = os.path.join(RUTA_FACTURAS, nombre_archivo)
        pdf.output(ruta)

        log_info(f"Factura PDF generada correctamente → ID: {id_factura}, Ruta: {ruta}")
        return ruta

    except Exception as e:
        log_error(f"Error al generar PDF de la factura ID {id_factura}: {e}")
        return None


def exportar_factura_interactivamente():
    """
    Permite al usuario exportar una factura a PDF de manera interactiva.

    Muestra una lista de facturas, permite seleccionar el ID de la factura y genera el archivo PDF correspondiente.
    """
    facturas = listar_facturas()
    if not facturas:
        mostrar_error("No hay facturas registradas.\n")
        return

    mostrar_facturas(facturas)

    while True:
        entrada = pedir_input_con_cancelacion("Ingresá el ID de la factura a exportar (C para cancelar): ")
        if entrada.lower() == "c":
            mostrar_cancelado("Ventas")
            return
        try:
            id_factura = int(entrada)
        except ValueError:
            mostrar_error("El ID debe ser un número.")
            continue
        ids = []
        for factura in facturas:
            ids.append(factura[0])
        if id_factura not in ids:
            mostrar_error("El ID de factura no existe.")
            continue
        break

    resultado = generar_pdf_factura(id_factura)
    mostrar_exito(f"Factura guardada en: {resultado}")
