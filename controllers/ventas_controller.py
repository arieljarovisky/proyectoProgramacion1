from flask import request, jsonify
import json
import os
from datetime import datetime
from controllers.caja_controller import cargar_caja, guardar_caja
import uuid

VENTAS_FILE = "data/ventas.json"
CAJA_FILE = "data/caja.json"
PRODUCTOS_FILE = "data/productos.json"

def cargar_productos():
    if not os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
# Cargar ventas desde el archivo JSON
def cargar_ventas():
    if not os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, "w") as f:
            json.dump([], f)
        return []

    with open(VENTAS_FILE, "r") as f:
        return json.load(f)


# Guardar ventas en el archivo JSON
def guardar_ventas(ventas):
    with open(VENTAS_FILE, "w") as f:
        json.dump(ventas, f, indent=2)

# Registrar una nueva venta
from flask import request, jsonify
from datetime import datetime
import json, os, uuid

VENTAS_FILE = "data/ventas.json"
CAJA_FILE = "data/caja.json"

def cargar_ventas():
    if not os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, "w") as f:
            json.dump([], f)
    with open(VENTAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_ventas(ventas):
    with open(VENTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ventas, f, indent=2, ensure_ascii=False)

def cargar_caja():
    if not os.path.exists(CAJA_FILE):
        with open(CAJA_FILE, "w") as f:
            json.dump({"saldo": 0, "movimientos": []}, f)
    with open(CAJA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_caja(caja):
    with open(CAJA_FILE, "w", encoding="utf-8") as f:
        json.dump(caja, f, indent=2, ensure_ascii=False)

def registrar_venta():
    data = request.get_json()
    if not data or "items" not in data or not isinstance(data["items"], list):
        return jsonify({"error": "Datos inválidos"}), 400

    productos = cargar_productos()
    items_detallados = []

    for item in data["items"]:
        prod = next((p for p in productos if p["id"] == item["id"]), None)
        if not prod:
            return jsonify({"error": f"Producto con id {item['id']} no encontrado"}), 404

        items_detallados.append({
            "id": item["id"],
            "nombre": prod.get("nombre", "Producto"),
            "cantidad": item["cantidad"],
            "precio_unitario": prod["precio"]
        })

    total = sum(i["cantidad"] * i["precio_unitario"] for i in items_detallados)
    venta_id = str(uuid.uuid4())
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nueva_venta = {
        "id": venta_id,
        "items": items_detallados,
        "total": total,
        "fecha": fecha_actual
    }

    # Guardar la venta
    ventas = cargar_ventas()
    ventas.append(nueva_venta)
    guardar_ventas(ventas)

    # Registrar ingreso en caja con mismo ID
    caja = cargar_caja()
    descripcion = f"Venta #{len([m for m in caja['movimientos'] if m['tipo'] == 'ingreso']) + 1}"
    nuevo_ingreso = {
        "id": venta_id,
        "tipo": "ingreso",
        "monto": total,
        "descripcion": descripcion,
        "fecha": fecha_actual
    }

    caja["saldo"] += total
    caja["movimientos"].append(nuevo_ingreso)
    guardar_caja(caja)

    return jsonify({"message": "Venta registrada", "venta": nueva_venta}), 201



# Obtener todas las ventas
def obtener_ventas():
    ventas = cargar_ventas()
    return jsonify(ventas), 200


# Actualizar una venta existente
def actualizar_venta(id):
    data = request.get_json()

    if not data or "items" not in data or "total" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    ventas = cargar_ventas()

    for venta in ventas:
        if venta["id"] == id:
            venta["items"] = data["items"]
            venta["total"] = data["total"]
            guardar_ventas(ventas)
            return jsonify({"message": "Venta actualizada correctamente"}), 200

    return jsonify({"error": "Venta no encontrada"}), 404


# Eliminar una venta por ID
def eliminar_venta(id):
    ventas = cargar_ventas()

    # Usamos lambda para filtrar las ventas que no tienen el mismo ID
    ventas_filtradas = list(filter(lambda venta: venta["id"] != id, ventas))

    if len(ventas_filtradas) == len(ventas):
        return jsonify({"error": "Venta no encontrada"}), 404

    guardar_ventas(ventas_filtradas)
    return jsonify({"message": "Venta eliminada correctamente"}), 200
