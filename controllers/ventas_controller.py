from flask import request, jsonify
import json
import os
from datetime import datetime
from controllers.productos_controller import cargar_productos, guardar_productos
from controllers.caja_controller import cargar_caja, guardar_caja
import uuid

VENTAS_FILE = "data/ventas.json"


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
def registrar_venta():
    data = request.get_json()

    if not data or "items" not in data or not isinstance(data["items"], list) or len(data["items"]) == 0 or "total" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    productos = cargar_productos()

    # Verificar stock y descontar
    for item in data["items"]:
        producto = next((p for p in productos if p["id"] == item["id"]), None)
        if not producto:
            return jsonify({"error": f"Producto con ID {item['id']} no encontrado"}), 404
        if producto["stock"] < item["cantidad"]:
            return jsonify({"error": f"Stock insuficiente para el producto '{producto['nombre']}'"}), 400
        producto["stock"] -= item["cantidad"]

    guardar_productos(productos)

    ventas = cargar_ventas()

    venta = {
        "id": str(uuid.uuid4()),
        "items": data["items"],
        "total": data["total"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    ventas.append(venta)
    guardar_ventas(ventas)
    caja = cargar_caja()
    ingreso = {
    "tipo": "ingreso",
    "monto": data["total"],
    "descripcion": f"Venta #{len(ventas) + 1}",
    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    caja["saldo"] += ingreso["monto"]
    caja["movimientos"].append(ingreso)
    guardar_caja(caja)

    return (
        jsonify({
            "message": "Venta registrada correctamente",
            "venta_id": venta["id"],
            "fecha": venta["fecha"],
        }),
        201,
    )


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
