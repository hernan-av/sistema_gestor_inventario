# Sistema de Gestión de Inventario

Aplicación de consola desarrollada en Python para la gestión integral de productos tecnológicos. Permite administrar clientes, proveedores, categorías, productos y facturación, todo desde una interfaz visual con estilo retro y terminal enriquecida gracias a la biblioteca `rich`.

Este sistema fue desarrollado siguiendo buenas prácticas de diseño, documentación y estructura modular.

---

## Funcionalidades principales

- Alta, modificación y baja de clientes, proveedores, categorías y productos.
- Registro de ventas y generación automática de facturas con detalle.
- Exportación de comprobantes en PDF con diseño limpio.
- Visualización clara de tablas y paneles estéticos retro tipo CRT.
- Validación robusta de entradas; cancelación segura con 'c'.
- Eliminación solo si no existen dependencias asociadas (seguridad referencial).
- Persistencia mediante SQLite — base lista desde el primer uso.

---

## Cómo ejecutar el sistema

1. Clonar o descargar el repositorio

```bash
git clone https://github.com/hernan-av/sistema_gestor_inventario.git
```

2. Crear y activar entorno virtual

```bash
python -m venv venv # Creación del entorno

venv\Scripts\activate # Ativación en Windows

source venv/bin/activate  # Ativación en Linux/macOS
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Ejecutar el programa

```bash
python main.py
```

El sistema se inicia con un menú interactivo por consola.

---

## Estructura del proyecto

```
core/                       # Utilidades generales
  └── logger.py
  └── utils.py
  └── validaciones_generales.py

db/                        # Conexión y creación de tablas
  └── data_base.py

gestor_categorias/         # Lógica de categorías
  └── categorias_db.py
  └── categorias_gestor.py
  └── categorias_validaciones.py

gestor_clientes/           # Lógica de clientes
  └── clientes_db.py
  └── clientes_gestor.py
  └── clientes_validaciones.py

gestor_productos/          # Lógica de productos
  └── productos_db.py
  └── productos_gestor.py
  └── productos_validaciones.py

gestor_proveedores/        # Lógica de proveedores
  └── proveedores_db.py
  └── proveedores_gestor.py
  └── proveedores_validaciones.py

gestor_ventas/             # Registro de ventas y facturas
  └── exportar_factura.py
  └── facturas_db.py
  └── ventas_gestor.py
  └── ventas_validaciones.py

interfaz/                  # Visuales y estética con Rich
  └── diseño_interfaz.py
  └── mostrar_resumen.py

insert_datos_prueba.py     # Datos ficticios de carga inicial
main.py                    # Bucle principal
requirements.txt           # Dependencias
README.md                  # Documentación del sistema
.gitignore                 # Exclusiones técnicas
```

---

## Diseño y consideraciones técnicas

- Código modular con separación de responsabilidades por entidad.
- Interfaz visual enriquecida con Rich: paneles, tablas, reglas, colores y feedback
- Validaciones iterativas, entradas seguras y manejo de excepciones.
- Registro de eventos importantes en registro.log.
- Docstrings en cada función según PEP257.
- Cumplimiento de PEP8 y aplicación del Zen de Python (“Simple is better than complex”)...

---

## Ejemplo visual de factura generada

Al confirmar una venta, el sistema imprime en consola un comprobante con estética tipo CRT retro, usando paneles alineados y tablas enriquecidas. Por ejemplo:

```
╭──────────────────────────────╮ ╭──────────────────────────────────╮
│  Factura # 3                 │ │  Cliente: Laura Martínez         │
│  Fecha: 2025-07-15 01:32:36  │ │  ID Cliente: 1                   │
│  Total: $90500.00            │ │  Email: laura.martinez@mail.com  │
╰──────────────────────────────╯ │  DNI: 40875231                   │
                                 ╰──────────────────────────────────╯

                         Detalle de productos vendidos
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Producto             ┃ Categoría   ┃ Cantidad ┃ Precio Unitario ┃  Subtotal ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Teclado mecánico RGB │ Periféricos │    1     │       $90500.00 │ $90500.00 │
└──────────────────────┴─────────────┴──────────┴─────────────────┴───────────┘
```

Además de mostrarse en consola, esta factura se guarda automáticamente como archivo PDF en disco. Es compatible con impresión o envío por correo.

---

## Datos precargados

El archivo `insert_datos_prueba.py` incluye registros ficticios para poblar automáticamente las tablas principales del sistema: clientes, productos, proveedores y categorías.

Al ejecutar este script, el sistema queda inmediatamente funcional y preparado para realizar pruebas completas como:

- Registrar ventas y generar facturas.
- Comprobar visualizaciones en consola (paneles y tablas estilo CRT).
- Verificar exportación en PDF.
- Validar que las reglas de eliminación segura funcionen correctamente.

Esta carga inicial facilita la evaluación del flujo general del sistema sin necesidad de ingresar datos manualmente.

---

## Posibles mejoras futuras

- Módulo de entregas/logística hacia el cliente
- Control de stock mínimo con alertas
- Inclusión de impuestos, descuentos o percepciones
- Métodos de pago, condiciones y vencimientos
- Envío automático del PDF por correo

## Requisitos

- Python 3.10+
- Biblioteca `rich`
- Biblioteca `fpdf`

Instalación rápida:

```
pip install -r requirements.txt
```

---

## Nota final

Este sistema representa el cierre del proceso formativo de Programación 1.

Fue diseñado con foco en la experiencia del usuario y en las buenas prácticas de desarrollo que facilitan el mantenimiento y la colaboración futura.

Más allá del código funcional, busca demostrar una manera de pensar como programador: lógica limpia, decisiones justificadas, y respeto por el legado que deja cada línea escrita.
