"""
Este archivo define y agrupa todas las rutas de la API de la aplicación Caja Plus mediante Blueprints de Flask.
Cada sección está separada por módulos funcionales: ventas, productos, caja, métricas, calculadora, pagos y facturas.
Cada ruta está asociada a una función de su respectivo controlador, permitiendo operaciones RESTful.
"""

# Importa Blueprint para agrupar rutas bajo un prefijo común
from flask import Blueprint

# Importa funciones del controlador de ventas
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta

# Importa función para obtener métricas
from controllers.metricas_controller import obtener_metricas

# Importa funciones del controlador de productos
from controllers.productos_controller import obtener_productos, registrar_producto, eliminar_producto, editar_producto

# Importa funciones del controlador de caja
from controllers.caja_controller import obtener_caja, registrar_ingreso, registrar_egreso

# Importa función del controlador de calculadora de precios
from controllers.calculadora_controller import calcular_precio

# Importa funciones del controlador de pagos
from controllers.pagos_controller import obtener_pagos, registrar_pago

# Importa funciones del controlador de facturas
from controllers.facturas_controller import generar_factura, descargar_pdf

# ---------- DEFINICIÓN DE BLUEPRINTS ----------

# Blueprint para las rutas relacionadas con ventas
ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

# Blueprint para las rutas de productos
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

# Blueprint para las rutas de caja
caja_bp = Blueprint('caja', __name__, url_prefix='/api/caja')

# Blueprint para la funcionalidad de calculadora de precios
calculadora_bp = Blueprint('calculadora', __name__, url_prefix='/api/calculadora')

# Blueprint para las rutas de pagos
pagos_bp = Blueprint('pagos', __name__, url_prefix='/api/pagos')
pagos_bp.route('', methods=['GET'])(obtener_pagos)    # Ruta para obtener todos los pagos
pagos_bp.route('', methods=['POST'])(registrar_pago)  # Ruta para registrar un nuevo pago

# ---------- RUTAS PARA VENTAS ----------

ventas_bp.route("/compras", methods=["POST"])(registrar_venta)   # Registrar nueva venta
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)     # Obtener todas las ventas (duplicada para compatibilidad)
ventas_bp.route('', methods=['GET'])(obtener_ventas)             # Alternativa para obtener todas las ventas
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)  # Actualizar una venta por ID
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta) # Eliminar una venta por ID

# ---------- RUTAS PARA PRODUCTOS ----------

productos_bp.route('', methods=['GET'])(obtener_productos)         # Obtener lista de productos
productos_bp.route('', methods=['POST'])(registrar_producto)       # Registrar nuevo producto
productos_bp.route('/<int:id>', methods=['DELETE'])(eliminar_producto)  # Eliminar producto por ID
productos_bp.route('/<int:id>', methods=['PUT'])(editar_producto)        # Editar producto por ID

# ---------- RUTA PARA MÉTRICAS ----------

ventas_bp.route("/metricas", methods=["GET"])(obtener_metricas)   # Obtener métricas generales de ventas

# ---------- RUTAS PARA CAJA ----------

caja_bp.route("/", methods=["GET"])(obtener_caja)             # Consultar el estado actual de la caja
caja_bp.route("/ingreso", methods=["POST"])(registrar_ingreso) # Registrar ingreso de dinero
caja_bp.route("/egreso", methods=["POST"])(registrar_egreso)   # Registrar egreso de dinero

# ---------- RUTA PARA CALCULADORA ----------

calculadora_bp.route("/calcular", methods=["POST"])(calcular_precio)  # Calcular precio final con IVA, envío y ganancia

# ---------- RUTAS PARA FACTURAS ----------

facturas_bp = Blueprint("facturas", __name__, url_prefix="/api/facturas")
facturas_bp.route("", methods=["POST"])(generar_factura)                        # Generar una factura nueva
facturas_bp.route("/pdf/<nombre_archivo>", methods=["GET"])(descargar_pdf)     # Descargar la factura en PDF
