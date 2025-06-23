"""
Este módulo gestiona las operaciones de ventas en la aplicación Caja Plus.
Incluye funciones para registrar, obtener, actualizar y eliminar ventas,
además de registrar el movimiento en caja y actualizar el stock de productos.
"""

# Importa funciones para manejar peticiones HTTP y respuestas JSON
from flask import request, jsonify

# Importa módulos del sistema para manipular archivos y generar IDs únicos
import json, os, uuid

# Importa datetime para registrar la fecha y hora de la venta
from datetime import datetime

# Importa funciones auxiliares para trabajar con caja y productos
from controllers.caja_controller import cargar_caja, guardar_caja
from controllers.productos_controller import cargar_productos, guardar_productos

# Rutas de los archivos JSON donde se guardan ventas y caja
VENTAS_FILE = "data/ventas.json"
CAJA_FILE = "data/caja.json"


# ---------- Función para cargar las ventas desde el archivo JSON ----------
def cargar_ventas():
    # Si no existe el archivo, se crea con una lista vacía
    if not os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Lee el archivo y devuelve las ventas como lista de diccionarios
    with open(VENTAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Función para guardar la lista de ventas en el archivo ----------
def guardar_ventas(ventas):
    # Guarda todas las ventas con formato legible (indentado)
    with open(VENTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ventas, f, indent=2, ensure_ascii=False)


# ---------- Función para registrar una nueva venta ----------
def registrar_venta():
    # Extrae los datos del body en formato JSON
    data = request.get_json()

    # Validación inicial: debe existir una lista de items
    if not data or "items" not in data or not isinstance(data["items"], list):
        return jsonify({"error": "Datos inválidos"}), 400
    
    # No se permite lista vacía de items
    if len(data["items"]) == 0:
        return jsonify({"error": "No se puede registrar una venta sin items"}), 400

    # Carga los productos existentes
    productos = cargar_productos()
    items_detallados = []

    # Recorre los items para validarlos y armar el detalle
    for item in data["items"]:
        prod = next((p for p in productos if str(p["id"]) == str(item["id"])), None)
        if not prod:
            return jsonify({"error": f"Producto con id {item['id']} no encontrado"}), 404

        items_detallados.append({
            "id": item["id"],
            "nombre": prod.get("nombre", "Producto"),
            "cantidad": item["cantidad"],
            "precio_unitario": prod["precio"]
        })

    # Calcula el total de la venta
    total = sum(i["cantidad"] * i["precio_unitario"] for i in items_detallados)

    # Genera un ID único para la venta y la fecha actual
    venta_id = str(uuid.uuid4())
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crea el diccionario de la nueva venta
    nueva_venta = {
        "id": venta_id,
        "items": items_detallados,
        "total": total,
        "fecha": fecha_actual
    }

    # Agrega la venta a la lista y la guarda en el archivo
    ventas = cargar_ventas()
    ventas.append(nueva_venta)
    guardar_ventas(ventas)

    # ---------- Registra el ingreso en la caja ----------
    caja = cargar_caja()

    # Se genera una descripción única para el movimiento
    descripcion = f"Venta #{len([m for m in caja['movimientos'] if m['tipo'] == 'ingreso']) + 1}"
    
    nuevo_ingreso = {
        "id": venta_id,
        "tipo": "ingreso",
        "monto": total,
        "descripcion": descripcion,
        "fecha": fecha_actual
    }

    # Actualiza el saldo y movimientos de caja
    caja["saldo"] += total
    caja["movimientos"].append(nuevo_ingreso)
    guardar_caja(caja)

    # ---------- Actualiza el stock de productos ----------
    for item in items_detallados:
        prod = next((p for p in productos if str(p["id"]) == str(item["id"])), None)
        if prod:
            prod["stock"] = max(0, prod.get("stock", 0) - item["cantidad"])

    # Guarda los productos actualizados
    guardar_productos(productos)

    # Devuelve la respuesta al frontend con la venta registrada
    return jsonify({"message": "Venta registrada", "venta": nueva_venta}), 201


# ---------- Obtener todas las ventas ----------
def obtener_ventas():
    ventas = cargar_ventas()                # Carga la lista de ventas
    return jsonify(ventas), 200             # Devuelve la lista en formato JSON


# ---------- Actualizar una venta existente ----------
def actualizar_venta(id):
    data = request.get_json()               # Obtiene los nuevos datos de la venta

    if not data or "items" not in data or "total" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    ventas = cargar_ventas()                # Carga ventas existentes

    for venta in ventas:
        if venta["id"] == id:
            venta["items"] = data["items"]  # Actualiza los ítems
            venta["total"] = data["total"]  # Actualiza el total
            guardar_ventas(ventas)          # Guarda los cambios
            return jsonify({"message": "Venta actualizada correctamente"}), 200

    return jsonify({"error": "Venta no encontrada"}), 404  # Si no se encontró la venta


# ---------- Eliminar una venta por ID ----------
def eliminar_venta(id):
    ventas = cargar_ventas()  # Carga ventas

    # Filtra la lista dejando fuera la venta con ese ID
    ventas_filtradas = list(filter(lambda venta: venta["id"] != id, ventas))

    # Si no cambió el largo, no se encontró el ID
    if len(ventas_filtradas) == len(ventas):
        return jsonify({"error": "Venta no encontrada"}), 404

    guardar_ventas(ventas_filtradas)  # Guarda la nueva lista
    return jsonify({"message": "Venta eliminada correctamente"}), 200
