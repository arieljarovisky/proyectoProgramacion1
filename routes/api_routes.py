from flask import Blueprint
from controllers.ventas_controller import registrar_venta, obtener_ventas, actualizar_venta, eliminar_venta

ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

# Ruta para registrar una nueva venta
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)

# Ruta para obtener todas las ventas
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)

# Ruta para editar las ventas
ventas_bp.route('/<int:id>', methods=['PUT'])(actualizar_venta)

# Ruta para eliminar ventas
ventas_bp.route('/<int:id>', methods=['DELETE'])(eliminar_venta)