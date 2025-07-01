"""
Controlador para gestionar los pagos y su registro como egresos en la caja.
- Permite consultar pagos y registrar nuevos pagos/egresos.
- Maneja la persistencia de pagos en un archivo JSON.
- Sincroniza cada pago con la caja (egreso).

Términos clave:
- Egreso: Salida de dinero de la caja (por pago de servicios, proveedores, etc).
- Pathlib: Módulo moderno de Python para manejo de rutas y archivos.
- JSON: Formato de intercambio de datos sencillo, ideal para persistencia ligera.
"""

import json
from flask import request, jsonify
from pathlib import Path
from datetime import datetime
from controllers.caja_controller import cargar_caja, guardar_caja

# Ruta al archivo donde se guardan los pagos
PAGOS_PATH = Path("./data/pagos.json")

def cargar_pagos():
    """
    Carga la lista de pagos desde el archivo JSON.
    Si el archivo no existe, lo crea vacío.
    
    Returns:
        list: Lista de pagos (cada pago es un dict).
    """
    if not PAGOS_PATH.exists():
        PAGOS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PAGOS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(PAGOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_pagos(pagos):
    """
    Guarda la lista de pagos en el archivo JSON.

    Args:
        pagos (list): Lista de pagos a guardar.
    """
    with open(PAGOS_PATH, "w", encoding="utf-8") as f:
        json.dump(pagos, f, indent=2, ensure_ascii=False)

def obtener_pagos():
    """
    Endpoint para consultar todos los pagos registrados.

    Returns:
        Response: JSON con la lista de pagos y código HTTP 200.
    """
    pagos = cargar_pagos()
    return jsonify(pagos), 200

def registrar_pago():
    """
    Endpoint para registrar un nuevo pago (egreso).

    Proceso:
    1. Valida los campos requeridos del request.
    2. Valida el monto (que sea numérico y > 0).
    3. Parsea y normaliza la fecha (acepta varios formatos).
    4. Agrega el pago al archivo de pagos.
    5. Registra un egreso en la caja.
    6. Retorna mensaje de éxito.

    Returns:
        Response: JSON de éxito o error, y código HTTP correspondiente.
    """
    data = request.get_json()
    campos_requeridos = ["destinatario", "concepto", "descripcion", "monto", "metodo"]

    # 1) Validar campos obligatorios
    for campo in campos_requeridos:
        if campo not in data or not isinstance(data[campo], str) or not data[campo].strip():
            if campo == "monto":  # Excepción para el monto (puede venir como número)
                if campo not in data or str(data[campo]).strip() == "":
                    return jsonify({"error": "Faltan campos requeridos"}), 400
            else:
                return jsonify({"error": f"El campo '{campo}' es obligatorio y no puede estar vacío"}), 400


    # 2) Validar y parsear monto
    try:
        monto = float(data["monto"])
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a cero"}), 400
    except Exception:
        return jsonify({"error": "El monto no es válido"}), 400

    # 3) Parsear fecha si viene, o usar ahora. NO PERMITIR FECHAS FUTURAS
    fecha_input = data.get("fecha")
    if fecha_input:
        fecha_str = fecha_input.strip()
        dt = None
        # Intentar varios formatos (ISO, DD/MM/YYYY, MM/DD/YYYY)
        try:
            dt = datetime.fromisoformat(fecha_str)
        except ValueError:
            try:
                dt_date = datetime.strptime(fecha_str, "%d/%m/%Y")
                now = datetime.now()
                dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
            except ValueError:
                try:
                    dt_date = datetime.strptime(fecha_str, "%m/%d/%Y")
                    now = datetime.now()
                    dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
                except ValueError:
                    return jsonify({
                        "error": "Formato de fecha inválido. Acepto YYYY-MM-DD, DD/MM/YYYY o MM/DD/YYYY"
                    }), 400
                    
        # Validar que la fecha no sea futura
        if dt.date() > datetime.now().date():
            return jsonify({"error": "No se permiten fechas futuras"}), 400
        fecha_pago = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4) Guardar en pagos.json
    pagos = cargar_pagos()
    nuevo_pago = {
        "id": str(len(pagos) + 1),
        "fecha": fecha_pago,
        "destinatario": data["destinatario"].strip(),
        "concepto": data["concepto"].strip(),
        "descripcion": data["descripcion"].strip(),
        "monto": monto,
        "metodo": data["metodo"].strip(),
    }
    pagos.append(nuevo_pago)
    guardar_pagos(pagos)


    # 5) Registrar egreso en caja.json (sincronización)
    caja = cargar_caja()
    egreso = {
        "id": nuevo_pago["id"],
        "tipo": "egreso",
        "monto": monto,
        "descripcion": data["descripcion"].strip(),
        "fecha": fecha_pago,
        "detalles": {
            "destinatario": data["destinatario"].strip(),
            "concepto": data["concepto"].strip(),
            "metodo": data["metodo"].strip(),
        },
    }
    caja["saldo"] -= monto
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Pago y egreso registrados correctamente"}), 201
