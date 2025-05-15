from flask import jsonify
from collections import defaultdict
from datetime import datetime
from controllers.ventas_controller import cargar_ventas
from controllers.pagos_controller import cargar_pagos

def obtener_metricas():
    ventas = cargar_ventas()
    pagos = cargar_pagos()
    total_egresos = sum(e.get('monto', 0) for e in pagos)
    total_ingresos = sum(v.get('total', 0) for v in ventas)
    total_ventas = len(ventas)
    total_pagos = len(pagos)
    total_items = 0
    producto_contador = defaultdict(int)
    ventas_por_dia = defaultdict(int)
    ventas_por_semana = defaultdict(int)
    ventas_por_mes = defaultdict(int)
    ventas_anuales= defaultdict(int)

    for venta in ventas:
        fecha_str = venta.get("fecha", "")[:10]  # yyyy-mm-dd
        ventas_por_dia[fecha_str] += 1
        fecha = datetime.strptime(venta.get("fecha", "")[:10], "%Y-%m-%d")
        semana = fecha.isocalendar().week
        mes = fecha.strftime("%Y-%m")  # Ej: 2025-04
        anio = fecha.year

        ventas_por_semana[f"Semana {semana} - {anio}"] += 1
        ventas_por_mes[mes] += 1
        ventas_anuales[str(anio)] += 1


        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            nombre = item.get("nombre", "Desconocido")
            total_items += cantidad
            producto_contador[nombre] += cantidad

    # Producto más vendido
    producto_mas_vendido = max(producto_contador.items(), key=lambda x: x[1], default=("Ninguno", 0))

    metricas = {
    # Totales generales
    "total_ventas": total_ventas,
    "total_pagos": total_pagos,
    "total_ingresos": total_ingresos,
    "total_egresos": total_egresos,

    # Desglose de ventas
    "total_items": total_items,
    "producto_mas_vendido": {
        "nombre": producto_mas_vendido[0],
        "cantidad": producto_mas_vendido[1]
    },

    # Distribución temporal
    "ventas_por_dia": dict(ventas_por_dia),
    "ventas_por_semana": dict(ventas_por_semana),
    "ventas_por_mes": dict(ventas_por_mes),
    "ventas_anuales": dict(ventas_anuales)
}

    return jsonify(metricas), 200
