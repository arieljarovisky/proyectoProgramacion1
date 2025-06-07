from flask import jsonify
from collections import defaultdict
from datetime import datetime
from controllers.ventas_controller import cargar_ventas
from controllers.caja_controller import cargar_caja

def obtener_metricas():
    ventas = cargar_ventas()
    caja = cargar_caja()
    movimientos = caja.get("movimientos", [])

    # Extraer egresos desde caja
    pagos = [mov for mov in movimientos if mov.get("tipo") == "egreso"]
    total_pagos = len(pagos)
    saldo_actual = caja.get("saldo", 0)

    # Totales
    total_ventas = len(ventas)
    total_items = 0
    total_ingresos = sum(v.get('total', 0) for v in ventas)
    total_egresos = sum(p.get('monto', 0) for p in pagos)

    # Métricas por período
    ventas_por_dia = defaultdict(int)
    ventas_por_semana = defaultdict(int)
    ventas_por_mes = defaultdict(int)
    ventas_anuales = defaultdict(int)

    ingresos_por_dia = defaultdict(float)
    ingresos_por_semana = defaultdict(float)
    ingresos_por_mes = defaultdict(float)
    ingresos_anuales = defaultdict(float)

    egresos_por_dia = defaultdict(float)
    egresos_por_semana = defaultdict(float)
    egresos_por_mes = defaultdict(float)
    egresos_anuales = defaultdict(float)

    producto_contador = defaultdict(int)

    for venta in ventas:
        fecha = datetime.strptime(venta.get("fecha", "")[:10], "%Y-%m-%d")
        total = venta.get("total", 0)
        fecha_str = fecha.strftime("%Y-%m-%d")
        semana = f"Semana {fecha.isocalendar().week} - {fecha.year}"
        mes = fecha.strftime("%Y-%m")
        anio = str(fecha.year)

        ventas_por_dia[fecha_str] += 1
        ingresos_por_dia[fecha_str] += total
        ventas_por_semana[semana] += 1
        ingresos_por_semana[semana] += total
        ventas_por_mes[mes] += 1
        ingresos_por_mes[mes] += total
        ventas_anuales[anio] += 1
        ingresos_anuales[anio] += total

        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            nombre = item.get("nombre", "Desconocido")
            total_items += cantidad
            producto_contador[nombre] += cantidad

    for pago in pagos:
        fecha = datetime.strptime(pago.get("fecha", "")[:10], "%Y-%m-%d")
        monto = pago.get("monto", 0)
        fecha_str = fecha.strftime("%Y-%m-%d")
        semana = f"Semana {fecha.isocalendar().week} - {fecha.year}"
        mes = fecha.strftime("%Y-%m")
        anio = str(fecha.year)

        egresos_por_dia[fecha_str] += monto
        egresos_por_semana[semana] += monto
        egresos_por_mes[mes] += monto
        egresos_anuales[anio] += monto

    producto_mas_vendido = max(producto_contador.items(), key=lambda x: x[1], default=("Ninguno", 0))

    metricas = {
        "saldo_actual": saldo_actual,
        "total_ventas": total_ventas,
        "total_pagos": total_pagos,
        "total_ingresos": total_ingresos,
        "total_egresos": total_egresos,
        "total_items": total_items,

        "producto_mas_vendido": {
            "nombre": producto_mas_vendido[0],
            "cantidad": producto_mas_vendido[1]
        },

        "ventas_por_dia": dict(ventas_por_dia),
        "ventas_por_semana": dict(ventas_por_semana),
        "ventas_por_mes": dict(ventas_por_mes),
        "ventas_anuales": dict(ventas_anuales),

        "ingresos_por_dia": dict(ingresos_por_dia),
        "ingresos_por_semana": dict(ingresos_por_semana),
        "ingresos_por_mes": dict(ingresos_por_mes),
        "ingresos_anuales": dict(ingresos_anuales),

        "egresos_por_dia": dict(egresos_por_dia),
        "egresos_por_semana": dict(egresos_por_semana),
        "egresos_por_mes": dict(egresos_por_mes),
        "egresos_anuales": dict(egresos_anuales),
    }

    return jsonify(metricas), 200
