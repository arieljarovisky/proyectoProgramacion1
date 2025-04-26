from flask import jsonify
from collections import defaultdict
from datetime import datetime
from controllers.ventas_controller import cargar_ventas

def obtener_metricas():
    ventas = cargar_ventas()

    total_ventas = len(ventas)
    total_items = 0
    producto_contador = defaultdict(int)
    ventas_por_dia = defaultdict(int)

    for venta in ventas:
        fecha_str = venta.get("fecha", "")[:10]  # yyyy-mm-dd
        ventas_por_dia[fecha_str] += 1

        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            nombre = item.get("nombre", "Desconocido")

            total_items += cantidad
            producto_contador[nombre] += cantidad

    # Producto más vendido
    producto_mas_vendido = max(producto_contador.items(), key=lambda x: x[1], default=("Ninguno", 0))

    metricas = {
        "total_ventas": total_ventas,
        "total_items": total_items,
        "producto_mas_vendido": {
            "nombre": producto_mas_vendido[0],
            "cantidad": producto_mas_vendido[1]
        },
        "ventas_por_dia": dict(ventas_por_dia)
    }

    return jsonify(metricas), 200
