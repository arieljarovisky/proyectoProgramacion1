import json
from flask import request, jsonify
from pathlib import Path
from datetime import datetime
from controllers.caja_controller import cargar_caja, guardar_caja

PAGOS_PATH = Path("./data/pagos.json")

def cargar_pagos():
    if not PAGOS_PATH.exists():
        PAGOS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PAGOS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(PAGOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_pagos(pagos):
    with open(PAGOS_PATH, "w", encoding="utf-8") as f:
        json.dump(pagos, f, indent=2, ensure_ascii=False)

def obtener_pagos():
    pagos = cargar_pagos()
    return jsonify(pagos), 200

def registrar_pago():
    data = request.get_json()
    campos_requeridos = ["destinatario", "concepto", "descripcion", "monto", "metodo"]

    # 1) Validar campos obligatorios
    if not data or not all(campo in data and data[campo] for campo in campos_requeridos):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # 2) Validar y parsear monto
    try:
        monto = float(data["monto"])
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a cero"}), 400
    except Exception:
        return jsonify({"error": "El monto no es válido"}), 400

    # 3) Parsear fecha si viene, o usar ahora
    fecha_input = data.get("fecha")
    if fecha_input:
        fecha_str = fecha_input.strip()
        dt = None
        # 1) ISO: '2025-06-02'
        try:
            dt = datetime.fromisoformat(fecha_str)
        except ValueError:
            # 2) DD/MM/YYYY
            try:
                dt_date = datetime.strptime(fecha_str, "%d/%m/%Y")
                now = datetime.now()
                dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
            except ValueError:
                # 3) MM/DD/YYYY
                try:
                    dt_date = datetime.strptime(fecha_str, "%m/%d/%Y")
                    now = datetime.now()
                    dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
                except ValueError:
                    return jsonify({
                        "error": "Formato de fecha inválido. Acepto YYYY-MM-DD, DD/MM/YYYY o MM/DD/YYYY"
                    }), 400
        fecha_pago = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4) Guardar en pagos.json
    pagos = cargar_pagos()
    nuevo_pago = {
        "id": str(len(pagos) + 1),
        "fecha": fecha_pago,
        "destinatario": data["destinatario"],
        "concepto": data["concepto"],
        "descripcion": data["descripcion"],
        "monto": monto,
        "metodo": data["metodo"],
    }
    pagos.append(nuevo_pago)
    guardar_pagos(pagos)

    # 5) Registrar egreso en caja.json
    caja = cargar_caja()
    egreso = {
        "id": nuevo_pago["id"],
        "tipo": "egreso",
        "monto": monto,
        "descripcion": data["descripcion"],
        "fecha": fecha_pago,
        "detalles": {
            "destinatario": data["destinatario"],
            "concepto": data["concepto"],
            "metodo": data["metodo"],
        },
    }
    caja["saldo"] -= monto
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Pago y egreso registrados correctamente"}), 201
