"""
Controlador para operaciones relacionadas con la caja (saldo, ingresos, egresos, movimientos).

Términos clave:
- Controller: Archivo encargado de la lógica para cada endpoint; conecta las rutas (routes) con las operaciones sobre los datos.
- JSON: Formato estándar para intercambiar datos. Acá usamos archivos JSON como base de datos sencilla.
- Saldo: Monto total disponible en la caja.
- Movimiento: Registro de una operación de ingreso o egreso en la caja.
- Ingreso: Entrada de dinero.
- Egreso: Salida de dinero.
- UUID: Identificador único universal, usado para asignar un ID a cada movimiento.

Funciones principales:
- cargar_caja: Lee el archivo de caja y lo devuelve como diccionario.
- guardar_caja: Guarda el estado de la caja en disco.
- obtener_caja: Devuelve el estado actual de la caja por API.
- registrar_ingreso: Agrega un ingreso (entrada de dinero) a la caja.
- registrar_egreso: Agrega un egreso (salida de dinero) a la caja.
"""

from flask import jsonify, request
import json
import os
import uuid
from datetime import datetime

CAJA_FILE = "data/caja.json"

# ---------- Utilidades de persistencia ----------

def cargar_caja():
    """
    Lee y retorna el estado actual de la caja desde el archivo JSON.
    Si el archivo no existe, lo crea con saldo 0 y sin movimientos.
    Returns:
        dict: Estado actual de la caja (saldo y movimientos).
    """
    if not os.path.exists(CAJA_FILE):
        with open(CAJA_FILE, "w") as f:
            json.dump({"saldo": 0, "movimientos": []}, f)
        return {"saldo": 0, "movimientos": []}

    with open(CAJA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_caja(caja):
    """
    Guarda el estado actual de la caja en el archivo JSON.

    Args:
        caja (dict): Estado de la caja a guardar.
    """
    with open(CAJA_FILE, "w", encoding="utf-8") as f:
        json.dump(caja, f, indent=2, ensure_ascii=False)

# ---------- Endpoints (API) ----------

def obtener_caja():
    """
    Devuelve el estado actual de la caja (saldo y movimientos) vía API.

    Returns:
        tuple: (json, status_code)
    """
    caja = cargar_caja()
    movimientos = caja.get("movimientos", [])
    
    # ORDENAR POR FECHA DESCENDENTE
    try:
        movimientos.sort(
            key=lambda m: datetime.strptime(m['fecha'], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
    except Exception:
        pass
    
    # FILTRO POR TIPO
    tipo = request.args.get("tipo")
    if tipo in ("ingreso", "egreso"):
        movimientos = [m for m in movimientos if m.get("tipo") == tipo]
    
    # PAGINACION
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except Exception:
        page = 1
        per_page = 10

    total = len(movimientos)
    start = (page - 1) * per_page
    end = start + per_page
    movimientos_paginados = movimientos[start:end]

    # Devuelve solo la página de movimientos pero también el saldo total
    return jsonify({
        "saldo": caja.get("saldo", 0),
        "movimientos": movimientos_paginados,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

def registrar_ingreso():
    """
    Registra un ingreso de dinero en la caja.

    Espera un JSON con al menos 'total' y 'descripcion'.
    Suma el monto al saldo, agrega un movimiento de tipo 'ingreso' y guarda la caja.

    Returns:
        tuple: (json, status_code)
    """
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
        "id": str(uuid.uuid4()),  # ID único para el movimiento
        "tipo": "ingreso",
        "monto": monto,
        "descripcion": f"Venta #{data['descripcion']}",
        "fecha":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    guardar_caja(caja)

    return jsonify({"message": "Ingreso registrado correctamente"}), 201

def registrar_egreso():
    """
    Registra un egreso de dinero en la caja.

    Espera un JSON con al menos 'total' y 'descripcion'.
    Resta el monto al saldo (puede ser negativo), agrega un movimiento de tipo 'egreso' y guarda la caja.
    Permite agregar detalles adicionales (destinatario, concepto, método de pago) si están presentes.

    Returns:
        tuple: (json, status_code)
    """
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

    # Detalles extra: destinatario, concepto, método (si están presentes)
    detalles = {k: data[k] for k in ["destinatario", "concepto", "metodo"] if k in data}
    if detalles:
        egreso["detalles"] = detalles

    caja["saldo"] -= monto  # Permite saldo negativo (egreso mayor al saldo actual)
    caja["movimientos"].append(egreso)
    guardar_caja(caja)

    return jsonify({"message": "Egreso registrado correctamente"}), 201
