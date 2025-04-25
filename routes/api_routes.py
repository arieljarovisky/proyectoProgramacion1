from flask import Blueprint
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta
from controllers.productos_controller import obtener_productos, registrar_producto

ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')

# Ruta para registrar una nueva venta
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)

# Ruta para obtener todas las ventas
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)

# Ruta para editar las ventas
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)

# Ruta para eliminar ventas
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta)

# Ruta para obtener todos los productos
productos_bp.route('', methods=['GET'])(obtener_productos)

# Ruta para registrar un nuevo producto
productos_bp.route('', methods=['POST'])(registrar_producto)