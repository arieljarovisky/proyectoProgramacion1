from flask import Blueprint
from controllers.ventas_controller import registrar_venta, obtener_ventas

ventas_bp = Blueprint("ventas", __name__)

# Ruta para registrar una nueva venta
ventas_bp.route("/compras", methods=["POST"])(registrar_venta)

# Ruta para obtener todas las ventas
ventas_bp.route("/compras", methods=["GET"])(obtener_ventas)
