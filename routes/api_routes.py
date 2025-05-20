from flask import Blueprint
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta
from controllers.metricas_controller import obtener_metricas
from controllers.productos_controller import obtener_productos, registrar_producto, eliminar_producto, editar_producto
from controllers.caja_controller import obtener_caja, registrar_ingreso, registrar_egreso
from controllers.calculadora_controller import calcular_precio  

# Blueprint para ventas
ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

# Blueprint para productos
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

# Blueprint para caja
caja_bp = Blueprint('caja', __name__, url_prefix='/api/caja')

# Blueprint para calculadora
calculadora_bp = Blueprint('calculadora', __name__, url_prefix='/api/calculadora')  # 👈 nuevo blueprint


# Rutas para ventas
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta)

# Ruta para métricas
ventas_bp.route("/metricas", methods=["GET"])(obtener_metricas)

# Rutas para productos
productos_bp.route('', methods=['GET'])(obtener_productos)
productos_bp.route('', methods=['POST'])(registrar_producto)
productos_bp.route('/<int:id>', methods=['DELETE'])(eliminar_producto)
productos_bp.route('/<int:id>', methods=['PUT'])(editar_producto)

# Rutas para caja
caja_bp.route("/", methods=["GET"])(obtener_caja)
caja_bp.route("/ingreso", methods=["POST"])(registrar_ingreso)
caja_bp.route("/egreso", methods=["POST"])(registrar_egreso)

# Rutas para calculadora
calculadora_bp.route("/calcular_precio", methods=["POST"])(calcular_precio)  
