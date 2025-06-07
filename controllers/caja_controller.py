from flask import jsonify, request
import json
import os
import uuid
from datetime import datetime

CAJA_FILE = "data/caja.json"

# ---------- Utilidades ----------
def cargar_caja():
    if not os.path.exists(CAJA_FILE):
        with open(CAJA_FILE, "w") as f:
            json.dump({"saldo": 0, "movimientos": []}, f)
        return {"saldo": 0, "movimientos": []}

    with open(CAJA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_caja(caja):
    with open(CAJA_FILE, "w", encoding="utf-8") as f:
        json.dump(caja, f, indent=2, ensure_ascii=False)

# ---------- Endpoints ----------
def obtener_caja():
    caja = cargar_caja()
    return jsonify(caja), 200

def registrar_ingreso():
    data = request.get_json()

    if not data or "monto" not in data or "descripcion" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Monto inválido"}), 400

    caja = cargar_caja()

    ingreso = {
        "id": str(uuid.uuid4()),
        "tipo": "ingreso",
        "monto": monto,
        "descripcion": data["descripcion"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    caja["saldo"] += monto
    caja["movimientos"].append(ingreso)
    guardar_caja(caja)

    return jsonify({"message": "Ingreso registrado correctamente"}), 201

def registrar_egreso():
    data = request.get_json()
    campos = ["descripcion", "monto"]

    if not data or not all(c in data and data[c] for c in campos):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Monto inválido"}), 400

    caja = cargar_caja()
    if monto > caja["saldo"]:
        return jsonify({"error": "Fondos insuficientes"}), 400

    egreso = {
        "id": str(uuid.uuid4()),
        "tipo": "egreso",
        "monto": monto,
        "descripcion": data["descripcion"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    detalles = {k: data[k] for k in ["destinatario", "concepto", "metodo"] if k in data}
    if detalles:
        egreso["detalles"] = detalles

    caja["saldo"] -= monto
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Egreso registrado correctamente"}), 201
