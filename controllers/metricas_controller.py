"""
Controlador encargado de calcular y exponer métricas del negocio para dashboards o reportes.
Incluye estadísticas de ventas y pagos agrupadas por diferentes períodos de tiempo.

Términos clave:
- Métrica: Valor cuantitativo para medir rendimiento (ej: ventas totales, egresos).
- Dashboard: Panel visual donde se muestran las métricas clave de la empresa.
- defaultdict: Tipo especial de diccionario de Python que inicializa automáticamente un valor por defecto.
"""

from flask import jsonify
from collections import defaultdict
from datetime import datetime, timedelta
from controllers.ventas_controller import cargar_ventas
from controllers.caja_controller import cargar_caja

# Diccionario de nombres de meses en español (para etiquetas de semana/mes)
MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def semana_label(fecha):
    """
    Devuelve una etiqueta en español que representa la semana de una fecha dada.

    Args:
        fecha (datetime): Fecha de referencia.

    Returns:
        str: Etiqueta de semana, ej. '10-16 marzo 2025'
    """
    start_of_week = fecha - timedelta(days=fecha.weekday())  # lunes de esa semana
    end_of_week = start_of_week + timedelta(days=6)          # domingo de esa semana
    mes = MESES_ES[start_of_week.month]
    label = f"{start_of_week.day}-{end_of_week.day} {mes} {end_of_week.year}"
    return label

def obtener_metricas():
    """
    Calcula y retorna todas las métricas del negocio:
    - Totales de ventas, pagos, ingresos, egresos, items y saldo.
    - Agrupaciones por día, semana, mes y año.
    - Producto más vendido.
    Se utiliza para alimentar los dashboards y reportes de la aplicación.

    Returns:
        Response: JSON con todas las métricas calculadas.
    """
    # Cargar ventas y estado de caja (donde están los movimientos y el saldo)
    ventas = cargar_ventas()
    caja = cargar_caja()
    movimientos = caja.get("movimientos", [])

    # Extraer los egresos (pagos) desde los movimientos de caja
    pagos = [mov for mov in movimientos if mov.get("tipo") == "egreso"]
    total_pagos = len(pagos)
    saldo_actual = caja.get("saldo", 0)

    # Variables acumuladoras
    total_ventas = len(ventas)
    total_items = 0
    total_ingresos = sum(v.get('total', 0) for v in ventas)
    total_egresos = sum(p.get('monto', 0) for p in pagos)

    # Diccionarios para acumular valores por períodos de tiempo
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

    producto_contador = defaultdict(int)  # Para encontrar el producto más vendido

    # Procesar ventas para calcular métricas por período
    for venta in ventas:
        # Convertir la fecha del string al objeto datetime
        fecha = datetime.strptime(venta.get("fecha", "")[:10], "%Y-%m-%d")
        total = venta.get("total", 0)
        fecha_str = fecha.strftime("%Y-%m-%d")
        semana = semana_label(fecha)
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

        # Contar productos vendidos
        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            nombre = item.get("nombre", "Desconocido")
            total_items += cantidad
            producto_contador[nombre] += cantidad

    # Procesar pagos para calcular egresos por período
    for pago in pagos:
        fecha = datetime.strptime(pago.get("fecha", "")[:10], "%Y-%m-%d")
        monto = pago.get("monto", 0)
        fecha_str = fecha.strftime("%Y-%m-%d")
        semana = semana_label(fecha)
        mes = fecha.strftime("%Y-%m")
        anio = str(fecha.year)

        egresos_por_dia[fecha_str] += monto
        egresos_por_semana[semana] += monto
        egresos_por_mes[mes] += monto
        egresos_anuales[anio] += monto

    # Determinar el producto más vendido
    producto_mas_vendido = max(producto_contador.items(), key=lambda x: x[1], default=("Ninguno", 0))

    # Construir diccionario final de métricas
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

    # Retornar las métricas en formato JSON (para el frontend o la API)
    return jsonify(metricas), 200
