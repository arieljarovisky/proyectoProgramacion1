"""
Este archivo define funciones para calcular métricas de ventas, ingresos y egresos 
en la aplicación Flask de Caja Plus.

Incluye:
- Cálculo de totales y estadísticas agrupadas por día, semana, mes y año.
- Identificación del producto más vendido.
- Consolidación de datos de `ventas.json` y `caja.json`.
- Respuesta en formato JSON con todos los indicadores económicos del sistema.

Utiliza:
- `defaultdict` para inicializar contadores automáticamente.
- `datetime` y `timedelta` para manipulación de fechas.
- Diccionario `MESES_ES` para mostrar nombres de meses en español.
"""
from flask import jsonify  # Para devolver respuestas JSON desde Flask.
from collections import defaultdict  # Permite crear diccionarios con valores por defecto.
from datetime import datetime, timedelta  # Para manejar fechas y operaciones temporales.
from controllers.ventas_controller import cargar_ventas  # Importa función que carga las ventas desde archivo.
from controllers.caja_controller import cargar_caja  # Importa función que carga los movimientos de caja.

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}# Diccionario para traducir números de mes a su nombre en español.

def semana_label(fecha):
    """
    Dada una fecha, genera una etiqueta de semana en formato 'DD-DD mes YYYY'.
    Ejemplo: para el 2025-06-12 → '9-15 junio 2025'.
    """
    start_of_week = fecha - timedelta(days=fecha.weekday())  # Lunes de la semana.
    end_of_week = start_of_week + timedelta(days=6)          # Domingo de la semana.
    mes = MESES_ES[start_of_week.month]  # Nombre del mes de inicio.
    label = f"{start_of_week.day}-{end_of_week.day} {mes} {end_of_week.year}"
    return label
def obtener_metricas():
    """
    Calcula y devuelve un conjunto de métricas consolidadas del sistema:
    - Totales: ventas, pagos, ingresos, egresos, ítems vendidos, saldo actual.
    - Agrupaciones por día, semana, mes y año.
    - Producto más vendido.
    """
    ventas = cargar_ventas()  # Lista de ventas desde archivo.
    caja = cargar_caja()  # Estado actual de la caja.
    movimientos = caja.get("movimientos", [])  # Lista de movimientos (ingresos y egresos).

    pagos = [mov for mov in movimientos if mov.get("tipo") == "egreso"]  # Filtra solo los egresos.
    total_pagos = len(pagos)
    saldo_actual = caja.get("saldo", 0)

    total_ventas = len(ventas)
    total_items = 0
    total_ingresos = sum(v.get('total', 0) for v in ventas)
    total_egresos = sum(p.get('monto', 0) for p in pagos)

    # Inicialización de contadores agrupados
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

    producto_contador = defaultdict(int)  # Contador de ítems vendidos por producto.

    for venta in ventas:
        fecha = datetime.strptime(venta.get("fecha", "")[:10], "%Y-%m-%d")  # Extrae la fecha (solo día).
        total = venta.get("total", 0)  # Total de esa venta.
        fecha_str = fecha.strftime("%Y-%m-%d")  # Fecha como string.
        semana = semana_label(fecha)  # Etiqueta de semana.
        mes = fecha.strftime("%Y-%m")  # Año-mes.
        anio = str(fecha.year)

        # Actualiza contadores de ventas e ingresos
        ventas_por_dia[fecha_str] += 1
        ingresos_por_dia[fecha_str] += total
        ventas_por_semana[semana] += 1
        ingresos_por_semana[semana] += total
        ventas_por_mes[mes] += 1
        ingresos_por_mes[mes] += total
        ventas_anuales[anio] += 1
        ingresos_anuales[anio] += total

        # Cuenta productos vendidos
        for item in venta.get("items", []):
            cantidad = item.get("cantidad", 0)
            nombre = item.get("nombre", "Desconocido")
            total_items += cantidad
            producto_contador[nombre] += cantidad

    for pago in pagos:
        fecha = datetime.strptime(pago.get("fecha", "")[:10], "%Y-%m-%d")  # Fecha del egreso.
        monto = pago.get("monto", 0)
        fecha_str = fecha.strftime("%Y-%m-%d")
        semana = semana_label(fecha)
        mes = fecha.strftime("%Y-%m")
        anio = str(fecha.year)

        # Actualiza contadores de egresos
        egresos_por_dia[fecha_str] += monto
        egresos_por_semana[semana] += monto
        egresos_por_mes[mes] += monto
        egresos_anuales[anio] += monto

    producto_mas_vendido = max(producto_contador.items(), key=lambda x: x[1], default=("Ninguno", 0))
    # Busca el producto con mayor cantidad de ventas.

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

    return jsonify(metricas), 200  # Devuelve todas las métricas en formato JSON con status 200 OK.

