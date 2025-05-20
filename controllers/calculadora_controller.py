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
