import json
import os
from flask import jsonify, request


# Ruta del archivo de productos
PRODUCTOS_FILE = 'data/productos.json'

def cargar_productos():
    """Carga los productos desde el archivo JSON."""
    if not os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    
    with open(PRODUCTOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_productos():
    """Devuelve la lista de productos cargados."""
    productos = cargar_productos()
    return jsonify(productos), 200

def guardar_productos(productos):
    """Guarda la lista de productos en el archivo JSON."""
    with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2)

def registrar_producto():
    """Registra un nuevo producto enviado por POST."""
    data = request.get_json()

    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    productos = cargar_productos()

    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": data['nombre'],
        "descripcion": data.get('descripcion', ''),
        "precio": data['precio'],
        "stock": data['stock'],
        "categoria": data.get('categoria', 'Sin categoría')
    }

    productos.append(nuevo_producto)
    guardar_productos(productos)

    return jsonify({
        "message": "Producto registrado correctamente",
        "producto_id": nuevo_producto["id"]
    }), 201
    
def eliminar_producto(id):
    productos=cargar_productos()
    productos_filtrados=list(filter(lambda producto:producto["id"]!=id, productos))

    if len(productos_filtrados)==len(productos):
        return jsonify({"error": "Producto no encontrado"}), 404
    
    guardar_productos(productos_filtrados)
    return jsonify({"message": "Producto eliminado correctamente"}), 200

def editar_producto(id):
    productos  = cargar_productos()
    data = request.get_json()
    
    producto_encontrado =  next((producto for producto in productos if producto["id"] == id), None)
    if producto_encontrado is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    # Actualizamos los campos que vienen en la solicitud
    producto_encontrado["nombre"] = data.get("nombre", producto_encontrado["nombre"])
    producto_encontrado["descripcion"] = data.get("descripcion", producto_encontrado["descripcion"])
    producto_encontrado["precio"] = data.get("precio", producto_encontrado["precio"])
    producto_encontrado["stock"] = data.get("stock", producto_encontrado["stock"])
    producto_encontrado["categoria"] = data.get("categoria", producto_encontrado["categoria"])
    
    guardar_productos(productos)
    
    return jsonify({"message": "Producto actualizado correctamente"}), 200
