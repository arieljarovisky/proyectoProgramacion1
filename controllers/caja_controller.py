"""
Este archivo implementa la lógica de control de caja en la aplicación Flask de Caja Plus.

Incluye:
- Lectura y escritura del archivo `caja.json`, donde se guarda el saldo actual y el historial de movimientos.
- Registro de ingresos y egresos con validaciones y estructura uniforme.
- Endpoint para obtener el estado actual de la caja en formato JSON.

Funciones principales:
- `cargar_caja()`: carga el estado actual de la caja desde el archivo; si no existe, lo inicializa.
- `guardar_caja(caja)`: guarda los datos actualizados de la caja en el archivo.
- `obtener_caja()`: endpoint GET que devuelve el saldo y los movimientos.
- `registrar_ingreso()`: endpoint POST para registrar un ingreso por venta.
- `registrar_egreso()`: endpoint POST para registrar un egreso, con soporte para detalles opcionales.

Características:
- Los movimientos se registran con un ID único (`uuid4`), fecha y descripción.
- El campo `descripcion` puede incluir número de venta o detalle de gasto.
- Se permite saldo negativo en caja al registrar egresos.
- Los movimientos se guardan cronológicamente dentro del array `movimientos`.

Archivos utilizados:
- `caja.json`: contiene el estado financiero de la caja (`saldo` + lista de `movimientos`).

Librerías utilizadas:
- `Flask`: para manejar peticiones HTTP (`request`, `jsonify`).
- `json`, `os`: para manejo de archivos.
- `uuid`: para generar identificadores únicos.
- `datetime`: para generar timestamps con la fecha y hora actual.
"""

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


def obtener_caja():
    caja = cargar_caja()
    return jsonify(caja), 200

def registrar_ingreso():
    data = request.get_json()
    print(data)
    if not data or "total" not in data or "descripcion" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        monto = float(data["total"])
        if monto <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Monto inválido"}), 400

    caja = cargar_caja()

    caja["saldo"] += monto
    caja["movimientos"].append({
        "id": str(uuid.uuid4()),  # <--- agregá esto
        "tipo": "ingreso",
        "monto": monto,
        "descripcion": f"Venta #{data["descripcion"]}",
        "fecha":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    guardar_caja(caja)

    return jsonify({"message": "Ingreso registrado correctamente"}), 201

def registrar_egreso():
    data = request.get_json()
    campos = ["descripcion", "total"]

    if not data or not all(c in data and data[c] for c in campos):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        monto = float(data["total"])
        if monto <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Monto inválido"}), 400

    caja = cargar_caja()

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

    caja["saldo"] -= monto  # ✅ Permite saldo negativo
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Egreso registrado correctamente"}), 201
