from rich.console import Console

from interfaz.diseño_interfaz import (
    mostrar_menu_principal,
    menu_ventas,
    menu_clientes,
    menu_proveedores,
    menu_productos,
    menu_categorias,
    mostrar_bienvenida,
    mostrar_error
)

from db.data_base import inicializar_base
from gestor_ventas.ventas_gestor import procesar_venta_interactiva, imprimir_detalle_venta
from gestor_ventas.exportar_factura import exportar_factura_interactivamente
from gestor_clientes.clientes_gestor import agregar_cliente, mostrar_todos_los_clientes, editar_cliente, borrar_cliente
from gestor_proveedores.proveedores_gestor import agregar_proveedor, mostrar_todos_los_proveedores, editar_proveedor, borrar_proveedor
from gestor_productos.productos_gestor import agregar_producto, mostrar_todos_los_productos, editar_producto, borrar_producto
from gestor_categorias.categorias_gestor import agregar_categoria, mostrar_todas_las_categorias, editar_categoria, borrar_categoria

console = Console()

def main():
    """
    Función principal del sistema de gestión de inventario.
    Inicializa la base de datos y presenta el menú principal al usuario.
    Dependiendo de la opción seleccionada, accede a los menús correspondientes
    para realizar operaciones sobre ventas, clientes, proveedores, productos o categorías.
    """
    inicializar_base()
    mostrar_bienvenida()

    while True:
        # Reseteo del encabezado del menú principal
        mostrar_menu_principal._encabezado_mostrado = False
        opcion_principal = mostrar_menu_principal()

        if opcion_principal == "1":  # Ventas
            menu_ventas._encabezado_mostrado = False
            while True:
                opcion = menu_ventas()
                if opcion == "1":
                    procesar_venta_interactiva()
                elif opcion == "2":
                    imprimir_detalle_venta()
                elif opcion == "3":
                    exportar_factura_interactivamente()
                elif opcion == "0":
                    break
                else:
                    mostrar_error("Opción inválida, vuelve a intentarlo.\n")

        elif opcion_principal == "2":  # Clientes
            menu_clientes._encabezado_mostrado = False
            while True:
                opcion = menu_clientes()
                if opcion == "1":
                    agregar_cliente()
                elif opcion == "2":
                    mostrar_todos_los_clientes()
                elif opcion == "3":
                    editar_cliente()
                elif opcion == "4":
                    borrar_cliente()
                elif opcion == "0":
                    break
                else:
                    mostrar_error("Opción inválida, vuelve a intentarlo.\n")

        elif opcion_principal == "3":  # Proveedores
            menu_proveedores._encabezado_mostrado = False
            while True:
                opcion = menu_proveedores()
                if opcion == "1":
                    agregar_proveedor()
                elif opcion == "2":
                    mostrar_todos_los_proveedores()
                elif opcion == "3":
                    editar_proveedor()
                elif opcion == "4":
                    borrar_proveedor()
                elif opcion == "0":
                    break
                else:
                    mostrar_error("Opción inválida, vuelve a intentarlo.\n")

        elif opcion_principal == "4":  # Productos
            menu_productos._encabezado_mostrado = False
            while True:
                opcion = menu_productos()
                if opcion == "1":
                    agregar_producto()
                elif opcion == "2":
                    mostrar_todos_los_productos()
                elif opcion == "3":
                    editar_producto()
                elif opcion == "4":
                    borrar_producto()
                elif opcion == "0":
                    break
                else:
                    mostrar_error("Opción inválida, vuelve a intentarlo.\n")

        elif opcion_principal == "5":  # Categorías
            menu_categorias._encabezado_mostrado = False
            while True:
                opcion = menu_categorias()
                if opcion == "1":
                    agregar_categoria()
                elif opcion == "2":
                    mostrar_todas_las_categorias()
                elif opcion == "3":
                    editar_categoria()
                elif opcion == "4":
                    borrar_categoria()
                elif opcion == "0":
                    break
                else:
                    mostrar_error("Opción inválida, vuelve a intentarlo.\n")

        elif opcion_principal == "0":
            console.print("\n[bold green]\n▌ ¡Gracias por usar el sistema de gestión![/bold green]\n")
            break

        else:
            mostrar_error("Opción inválida, vuelve a intentarlo.")

if __name__ == "__main__":
    main()
