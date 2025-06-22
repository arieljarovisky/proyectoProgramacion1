"""
ventas_controller.py

Controlador para operaciones de ventas del sistema Caja Plus.

Responsabilidades principales:
- Permite registrar, obtener, actualizar y eliminar ventas.
- Actualiza el stock de productos y registra el ingreso de dinero en caja.
- Persiste datos en archivos JSON, funcionando como una "base de datos ligera".

Conceptos clave:
- CRUD: Create, Read, Update, Delete (Crear, Leer, Actualizar, Eliminar).
- Endpoint: Punto de acceso a una funcionalidad del backend vía HTTP.
- UUID: Identificador único universal, asegura que cada venta tenga un ID único y no colisione con otros registros.
- Stock: Cantidad de productos disponibles. Cada venta descuenta del stock.
- Para propósitos didácticos, la persistencia es en archivos JSON. En producción, se debe usar una base de datos real y lógica transaccional robusta.
"""

from flask import request, jsonify
import json, os, uuid
from datetime import datetime
from controllers.caja_controller import cargar_caja, guardar_caja
from controllers.productos_controller import cargar_productos, guardar_productos

VENTAS_FILE = "data/ventas.json"
CAJA_FILE = "data/caja.json"

def cargar_ventas():
    """
    Carga todas las ventas desde el archivo JSON correspondiente.

    Returns:
        list: Lista de ventas registradas.
    """
    if not os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(VENTAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_ventas(ventas):
    """
    Guarda la lista de ventas en el archivo JSON correspondiente.

    Args:
        ventas (list): Lista de ventas a guardar.
    """
    with open(VENTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ventas, f, indent=2, ensure_ascii=False)

def registrar_venta():
    """
    Endpoint para registrar una nueva venta.

    Proceso:
    - Valida que existan items en la venta.
    - Valida que los productos existan y tengan stock suficiente.
    - Calcula el total de la venta.
    - Genera un UUID único para la venta.
    - Registra la venta en ventas.json.
    - Registra el ingreso en caja.json (movimiento).
    - Descuenta el stock de cada producto.
    - Devuelve la venta registrada y mensaje de éxito.

    Returns:
        Response: Mensaje de éxito o error y la venta registrada.
    """
    data = request.get_json()
    if not data or "items" not in data or not isinstance(data["items"], list):
        return jsonify({"error": "Datos inválidos"}), 400
    
    # No permitimos lista vacía de items
    if len(data["items"]) == 0:
        return jsonify({"error": "No se puede registrar una venta sin items"}), 400

    # Cargamos los productos
    productos = cargar_productos()
    items_detallados = []

    # Validamos y armamos el detalle
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

    # Calculamos el total y armamos la venta
    total = sum(i["cantidad"] * i["precio_unitario"] for i in items_detallados)
    venta_id = str(uuid.uuid4())
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nueva_venta = {
        "id": venta_id,
        "items": items_detallados,
        "total": total,
        "fecha": fecha_actual
    }

    # Guardamos la venta
    ventas = cargar_ventas()
    ventas.append(nueva_venta)
    guardar_ventas(ventas)

    # Registramos el ingreso en caja.json
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
    
    # Actualizamos el stock en productos.json
    for item in items_detallados:
        prod = next((p for p in productos if str(p["id"]) == str(item["id"])), None)
        if prod:
            prod["stock"] = max(0, prod.get("stock", 0) - item["cantidad"])
    
    guardar_productos(productos)

    # Devolvemos la respuesta al frontend
    return jsonify({"message": "Venta registrada", "venta": nueva_venta}), 201

def obtener_ventas():
    """
    Endpoint para obtener todas las ventas registradas.

    Returns:
        Response: Lista de ventas y status 200.
    """
    ventas = cargar_ventas()
    return jsonify(ventas), 200

def actualizar_venta(id):
    """
    Endpoint para actualizar una venta existente.

    Args:
        id (str): ID de la venta a actualizar.

    Proceso:
    - Valida que existan los campos necesarios.
    - Busca la venta por ID y actualiza sus items y total.
    - Guarda los cambios en ventas.json.

    Returns:
        Response: Mensaje de éxito o error.
    """
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

def eliminar_venta(id):
    """
    Endpoint para eliminar una venta por su ID.

    Args:
        id (str): ID de la venta a eliminar.

    Proceso:
    - Filtra la lista de ventas eliminando la que tenga el ID dado.
    - Guarda la nueva lista en ventas.json.

    Returns:
        Response: Mensaje de éxito o error.
    """
    ventas = cargar_ventas()

    # Usamos lambda para filtrar las ventas que no tienen el mismo ID
    ventas_filtradas = list(filter(lambda venta: venta["id"] != id, ventas))

    if len(ventas_filtradas) == len(ventas):
        return jsonify({"error": "Venta no encontrada"}), 404

    guardar_ventas(ventas_filtradas)
    
    return jsonify({"message": "Venta eliminada correctamente"}), 200

