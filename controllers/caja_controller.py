from flask import jsonify, request
import json
import os
from datetime import datetime

CAJA_FILE = "data/caja.json"

# Cargar caja desde el archivo JSON
def cargar_caja():
    if not os.path.exists(CAJA_FILE):
        with open(CAJA_FILE, "w") as f:
            json.dump({"saldo": 0, "movimientos": []}, f)
        return {"saldo": 0, "movimientos": []}

    with open(CAJA_FILE, "r") as f:
        return json.load(f)

# Guardar caja en el archivo JSON
def guardar_caja(caja):
    with open(CAJA_FILE, "w") as f:
        json.dump(caja, f, indent=2)

# Obtener el estado actual de la caja
def obtener_caja():
    caja = cargar_caja()
    return jsonify(caja), 200

# Registrar un ingreso en la caja
def registrar_ingreso():
    data = request.get_json()

    if not data or "monto" not in data or "descripcion" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    caja = cargar_caja()

    ingreso = {
        "tipo": "ingreso",
        "monto": data["monto"],
        "descripcion": data["descripcion"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    caja["saldo"] += ingreso["monto"]
    caja["movimientos"].append(ingreso)
    guardar_caja(caja)

    return jsonify({"message": "Ingreso registrado correctamente"}), 201

def registrar_egreso():
    data = request.get_json()

    if not data or "monto" not in data or "descripcion" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    caja = cargar_caja()

    if data["monto"] > caja["saldo"]:
        return jsonify({"error": "Fondos insuficientes"}), 400

    egreso = {
        "tipo": "egreso",
        "monto": data["monto"],
        "descripcion": data["descripcion"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    caja["saldo"] -= egreso["monto"]
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Egreso registrado correctamente"}), 201
