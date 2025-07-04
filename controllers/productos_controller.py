"""
Controlador para la gestión CRUD de productos en el sistema.
Todas las operaciones usan un archivo JSON como base de datos liviana.

Términos clave:
- CRUD: Sigla en inglés para Create (crear), Read (leer), Update (actualizar) y Delete (eliminar).
- JSON: Formato de archivo ligero, ideal para persistencia de datos estructurados de forma sencilla.
"""

import json
import os
from flask import jsonify, request

# Ruta del archivo de productos
PRODUCTOS_FILE = 'data/productos.json'

def cargar_productos():
    """
    Carga la lista de productos desde el archivo JSON.
    Si el archivo no existe, lo crea vacío.

    Returns:
        list: Lista de productos, cada uno representado como un diccionario.
    """
    if not os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    
    with open(PRODUCTOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_productos():
    """
    Endpoint para obtener todos los productos registrados.

    Returns:
        Response: JSON con la lista de productos y código HTTP 200.
    """
    productos = cargar_productos()
    
    
    # --- FILTRO POR NOMBRE (search) ---
    search = request.args.get("search", "").strip().lower()
    if search:
        productos = [
            p for p in productos
            if search in p["nombre"].lower() or search in p.get("descripcion", "").lower()
        ]
        
    # --- Paginación ---
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except Exception:
        page = 1
        per_page = 10

    total = len(productos)
    start = (page - 1) * per_page
    end = start + per_page
    productos_paginados = productos[start:end]

    return jsonify({
        "productos": productos_paginados,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

def guardar_productos(productos):
    """
    Guarda la lista completa de productos en el archivo JSON.

    Args:
        productos (list): Lista de productos a persistir.
    """
    with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2)

def registrar_producto():
    """
    Endpoint para registrar (crear) un nuevo producto.
    Agrega validaciones estrictas en los datos recibidos.
    """
    data = request.get_json()

    # Validar existencia de campos obligatorios
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    nombre = data['nombre']
    precio = data['precio']
    stock = data['stock']

    # Validaciones específicas
    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"error": "El nombre es obligatorio"}), 400
    if not (isinstance(precio, (int, float)) and precio > 0):
        return jsonify({"error": "El precio debe ser un número positivo"}), 400
    if not (isinstance(stock, int) and stock >= 0):
        return jsonify({"error": "El stock debe ser un entero mayor o igual a 0"}), 400

    productos = cargar_productos()

    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": nombre.strip(),
        "descripcion": data.get('descripcion', ''),
        "precio": precio,
        "stock": stock,
        "categoria": data.get('categoria', 'Sin categoría')
    }

    productos.append(nuevo_producto)
    guardar_productos(productos)

    return jsonify({
        "message": "Producto registrado correctamente",
        "producto_id": nuevo_producto["id"]
    }), 201
    
def eliminar_producto(id):
    """
    Endpoint para eliminar un producto por ID.

    Args:
        id (int): ID del producto a eliminar.

    Returns:
        Response: Mensaje de éxito si lo elimina, o error si no lo encuentra.
    """
    productos = cargar_productos()
    productos_filtrados = list(filter(lambda producto: producto["id"] != id, productos))

    if len(productos_filtrados) == len(productos):
        return jsonify({"error": "Producto no encontrado"}), 404
    
    guardar_productos(productos_filtrados)
    return jsonify({"message": "Producto eliminado correctamente"}), 200

def editar_producto(id):
    """
    Endpoint para editar los datos de un producto.
    Suma validaciones estrictas en los campos editados.
    """
    productos  = cargar_productos()
    data = request.get_json()
    
    producto_encontrado = next((producto for producto in productos if producto["id"] == id), None)
    if producto_encontrado is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Validar nombre, precio y stock solo si vienen en el request
    if "nombre" in data:
        if not isinstance(data["nombre"], str) or not data["nombre"].strip():
            return jsonify({"error": "El nombre es obligatorio"}), 400
    if "precio" in data:
        if not (isinstance(data["precio"], (int, float)) and data["precio"] > 0):
            return jsonify({"error": "El precio debe ser un número positivo"}), 400
    if "stock" in data:
        if not (isinstance(data["stock"], int) and data["stock"] >= 0):
            return jsonify({"error": "El stock debe ser un entero mayor o igual a 0"}), 400

    # Actualizamos solo los campos enviados (ya validados)
    producto_encontrado["nombre"] = data.get("nombre", producto_encontrado["nombre"])
    producto_encontrado["descripcion"] = data.get("descripcion", producto_encontrado["descripcion"])
    producto_encontrado["precio"] = data.get("precio", producto_encontrado["precio"])
    producto_encontrado["stock"] = data.get("stock", producto_encontrado["stock"])
    producto_encontrado["categoria"] = data.get("categoria", producto_encontrado["categoria"])
    
    guardar_productos(productos)
    
    return jsonify({"message": "Producto actualizado correctamente"}), 200
