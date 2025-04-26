from flask import Blueprint
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta
from controllers.metricas_controller import obtener_metricas
from controllers.productos_controller import obtener_productos, registrar_producto
from controllers.caja_controller import obtener_caja, registrar_ingreso, registrar_egreso

# Blueprint para ventas
ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

# Blueprint para productos
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

# Blueprint para caja
caja_bp = Blueprint('caja', __name__, url_prefix='/api/caja')


# Rutas para ventas
# Ruta para registrar una nueva venta
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)

# Ruta para obtener todas las ventas
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)

# Ruta para editar las ventas
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)

# Ruta para eliminar ventas
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta)

# Rutas para productos
# Ruta para obtener todos los productos
productos_bp.route('', methods=['GET'])(obtener_productos)

# Ruta para registrar un nuevo producto
productos_bp.route('', methods=['POST'])(registrar_producto)

# Ruta para obtener métricas
ventas_bp.route("/metricas", methods=["GET"])(obtener_metricas)

# Rutas para caja
# Ruta para obtener el estado de la caja
caja_bp.route("/", methods=["GET"])(obtener_caja)

# Ruta para registrar un ingreso en la caja
caja_bp.route("/ingreso", methods=["POST"])(registrar_ingreso)

# Ruta para registrar un egreso en la caja
caja_bp.route("/egreso", methods=["POST"])(registrar_egreso)
