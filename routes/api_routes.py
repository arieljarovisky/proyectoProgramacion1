"""
Define y agrupa todas las rutas (endpoints) principales de la API de Caja Plus utilizando Blueprints de Flask.

Cada grupo de rutas está asociado a una funcionalidad del sistema (ventas, productos, caja, pagos, facturas, etc.) y delega la lógica a los controladores correspondientes.

Términos clave:
- Blueprint: Es una forma de modularizar las rutas/endpoints de Flask, permitiendo dividir el código en componentes independientes y reutilizables.
- Endpoint: Es una URL específica de la API a la que el frontend o cualquier cliente puede hacer una solicitud HTTP (GET, POST, PUT, DELETE).
- Controller (controlador): Es el módulo encargado de la lógica para cada tipo de operación (por ejemplo, ventas, productos, caja).

Este archivo **NO contiene lógica de negocio**, solo define las rutas y las vincula con su respectivo controlador.
"""

from flask import Blueprint
# Importación de controladores (cada uno maneja la lógica para su dominio)
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta
from controllers.metricas_controller import obtener_metricas
from controllers.productos_controller import obtener_productos, registrar_producto, eliminar_producto, editar_producto
from controllers.caja_controller import obtener_caja, registrar_ingreso, registrar_egreso, eliminar_movimiento
from controllers.calculadora_controller import calcular_precio
from controllers.pagos_controller import obtener_pagos, registrar_pago
from controllers.facturas_controller import generar_factura, descargar_pdf

# ============================
# Blueprints por funcionalidad
# ============================

# Grupo de rutas para VENTAS y MÉTRICAS
ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

# Grupo de rutas para PRODUCTOS
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

# Grupo de rutas para CAJA
caja_bp = Blueprint('caja', __name__, url_prefix='/api/caja')

# Grupo de rutas para CALCULADORA (servicio adicional, por ejemplo, para calcular precios)
calculadora_bp = Blueprint('calculadora', __name__, url_prefix='/api/calculadora')

# Grupo de rutas para PAGOS (egresos)
pagos_bp = Blueprint('pagos', __name__, url_prefix='/api/pagos')
pagos_bp.route('', methods=['GET'])(obtener_pagos)   # Listar todos los pagos registrados
pagos_bp.route('', methods=['POST'])(registrar_pago) # Registrar un nuevo pago

# ========================
# Rutas para Ventas
# ========================

# POST /api/ventas/compras  --> Registrar nueva venta
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)

# GET /api/ventas/compras  --> Listar todas las ventas
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)

# GET /api/ventas  --> Listar todas las ventas (ruta alternativa, útil para simplificar el frontend)
ventas_bp.route('', methods=['GET'])(obtener_ventas)

# PUT /api/ventas/<id>  --> Editar venta existente
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)

# DELETE /api/ventas/<id>  --> Eliminar venta existente
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta)

# GET /api/ventas/metricas  --> Obtener métricas de ventas, ingresos, egresos, productos, etc.
ventas_bp.route("/metricas", methods=["GET"])(obtener_metricas)

# ========================
# Rutas para Productos
# ========================

productos_bp.route('', methods=['GET'])(obtener_productos)        # Listar productos
productos_bp.route('', methods=['POST'])(registrar_producto)      # Agregar nuevo producto
productos_bp.route('/<int:id>', methods=['DELETE'])(eliminar_producto)  # Eliminar producto por ID
productos_bp.route('/<int:id>', methods=['PUT'])(editar_producto)       # Editar producto por ID

# ========================
# Rutas para Caja
# ========================

caja_bp.route("/", methods=["GET"])(obtener_caja)                   # Consultar estado de la caja
caja_bp.route("/ingreso", methods=["POST"])(registrar_ingreso)      # Registrar un ingreso a la caja
caja_bp.route("/egreso", methods=["POST"])(registrar_egreso)        # Registrar un egreso de la caja
caja_bp.route("/movimiento/<id>", methods=["DELETE"])(eliminar_movimiento)  # Eliminar movimiento de la caja


# ========================
# Rutas para Calculadora
# ========================

calculadora_bp.route("/calcular", methods=["POST"])(calcular_precio) # Calcular precio, utilidad, etc.

# ========================
# Rutas para Facturas
# ========================

facturas_bp = Blueprint("facturas", __name__, url_prefix="/api/facturas")
facturas_bp.route("", methods=["POST"])(generar_factura)                      # Generar nueva factura
facturas_bp.route("/pdf/<nombre_archivo>", methods=["GET"])(descargar_pdf)    # Descargar PDF de factura

# NOTA:
# Este archivo solo define las rutas y blueprints. Los blueprints se registran en la aplicación principal (app.py).
