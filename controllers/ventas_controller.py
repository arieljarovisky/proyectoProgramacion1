from flask import request, jsonify
import json
import os

VENTAS_FILE = 'data/ventas.json'

# Cargar ventas desde el archivo JSON
def cargar_ventas():
    if not os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, 'w') as f:
            json.dump([], f)
        return []

    with open(VENTAS_FILE, 'r') as f:
        return json.load(f)

# Guardar ventas en el archivo JSON
def guardar_ventas(ventas):
    with open(VENTAS_FILE, 'w') as f:
        json.dump(ventas, f, indent=2)

# Registrar una nueva venta
def registrar_venta():
    data = request.get_json()

    if not data or 'items' not in data or 'total' not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    ventas = cargar_ventas()

    venta = {
        "id": len(ventas) + 1,
        "items": data['items'],
        "total": data['total']
    }

    ventas.append(venta)
    guardar_ventas(ventas)

    return jsonify({
        "message": "Venta registrada correctamente",
        "venta_id": venta["id"]
    }), 201

# Obtener todas las ventas
def obtener_ventas():
    ventas = cargar_ventas()
    return jsonify(ventas), 200
    