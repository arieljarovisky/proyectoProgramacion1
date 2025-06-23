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


