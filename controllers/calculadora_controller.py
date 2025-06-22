"""
Controlador que permite calcular el precio final de un producto considerando
costo, envío, margen de ganancia e IVA. Además, guarda el historial de cálculos realizados.

Términos clave:
- Controller: Se encarga de la lógica de negocio asociada a un endpoint.
- IVA: Impuesto al Valor Agregado, en Argentina suele ser del 21%.
- Margen de ganancia: Porcentaje que se suma al costo total para obtener una ganancia.
- Historial: Registro en archivo JSON con cada cálculo de precio realizado.
"""

import json
import os
from datetime import datetime

HISTORIAL_PATH = 'historial_precios.json'

def guardar_en_historial(entry):
    """
    Agrega una nueva entrada al historial de cálculos de precios.

    Si el archivo no existe, lo crea con una lista vacía.
    Cada entrada contiene información sobre el cálculo realizado.

    Args:
        entry (dict): Datos del cálculo a guardar.
    """
    if not os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, 'w') as f:
            json.dump([], f, indent=2)

    with open(HISTORIAL_PATH, 'r') as f:
        historial = json.load(f)

    historial.append(entry)

    with open(HISTORIAL_PATH, 'w') as f:
        json.dump(historial, f, indent=2)

def calcular_precio(data):
    """
    Calcula el precio final de un producto sumando costo, costo de envío,
    margen de ganancia y aplicando IVA (21%). Guarda el resultado en el historial.

    Args:
        data (dict): Debe contener 'costo_producto', 'costo_envio', 'margen_ganancia' (en %).

    Returns:
        float: Precio final redondeado a dos decimales.
    """
    costo_producto = float(data['costo_producto'])
    costo_envio = float(data['costo_envio'])
    margen_ganancia = float(data['margen_ganancia']) / 100

    iva = 0.21  # 21% de IVA
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
