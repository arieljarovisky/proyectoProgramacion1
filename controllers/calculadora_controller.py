"""
Este archivo define funciones para calcular precios finales de productos y guardar el historial
de dichos cálculos en un archivo JSON (`historial_precios.json`), dentro del sistema Caja Plus.

Incluye:
- `calcular_precio(data)`: calcula el precio final de un producto a partir del costo, envío, margen e IVA.
- `guardar_en_historial(entry)`: guarda cada resultado de cálculo con fecha y detalles en un historial persistente.

Características:
- El precio final se calcula aplicando un 21% de IVA y un margen de ganancia sobre el costo total.
- Cada entrada registrada incluye: costo del producto, costo de envío, margen aplicado, precio final y fecha.
- Si el archivo `historial_precios.json` no existe, se crea automáticamente.

Utiliza:
- `datetime` para generar la fecha y hora del cálculo.
- `json` y `os` para manipulación segura de archivos.
"""

import json
import os
from datetime import datetime

HISTORIAL_PATH = 'historial_precios.json'

def guardar_en_historial(entry):
    if not os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, 'w') as f:
            json.dump([], f, indent=2)

    with open(HISTORIAL_PATH, 'r') as f:
        historial = json.load(f)

    historial.append(entry)

    with open(HISTORIAL_PATH, 'w') as f:
        json.dump(historial, f, indent=2)

def calcular_precio(data):
    costo_producto = float(data['costo_producto'])
    costo_envio = float(data['costo_envio'])
    margen_ganancia = float(data['margen_ganancia']) / 100

    iva = 0.21
    base = costo_producto + costo_envio
    precio_final = base * (1 + iva) * (1 + margen_ganancia)

    resultado = {
        'costo_producto': costo_producto,
        'costo_envio': costo_envio,
        'margen_ganancia': margen_ganancia * 100,
        'precio_final': round(precio_final, 2),
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    guardar_en_historial(resultado)

    return resultado['precio_final']
