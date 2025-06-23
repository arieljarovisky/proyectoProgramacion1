"""
Este módulo gestiona el CRUD de productos para la aplicación Caja Plus.
Permite cargar, registrar, editar, eliminar y listar productos, trabajando
con un archivo JSON (`productos.json`) ubicado en la carpeta `data/`.

Cada función valida los datos de entrada y actualiza el archivo de productos
según corresponda. Las respuestas se devuelven en formato JSON para integrarse
con el frontend a través de una API.
"""

# Importa módulos necesarios para manipulación de archivos y manejo de peticiones/respuestas
import json
import os
from flask import jsonify, request

# Ruta al archivo JSON donde se almacenan los productos
PRODUCTOS_FILE = 'data/productos.json'


# ----------- Función para cargar productos desde el archivo JSON -----------
def cargar_productos():
    """Carga la lista de productos desde el archivo productos.json. Si no existe, lo crea vacío."""
    if not os.path.exists(PRODUCTOS_FILE):
        with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

    with open(PRODUCTOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# ----------- Función para obtener todos los productos -----------
def obtener_productos():
    """Devuelve todos los productos en formato JSON."""
    productos = cargar_productos()
    return jsonify(productos), 200


# ----------- Función para guardar productos en el archivo JSON -----------
def guardar_productos(productos):
    """Guarda la lista actualizada de productos en el archivo productos.json."""
    with open(PRODUCTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=2)


# ----------- Función para registrar un nuevo producto -----------
def registrar_producto():
    """
    Registra un nuevo producto recibido desde el frontend.
    Valida que el JSON tenga nombre, precio y stock.
    Luego lo agrega a la lista de productos con ID autoincremental.
    """
    data = request.get_json()

    # Validación básica de datos
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


# ----------- Función para eliminar un producto por ID -----------
def eliminar_producto(id):
    """
    Elimina un producto de la lista según su ID.
    Si no lo encuentra, devuelve error 404.
    """
    productos = cargar_productos()
    
    # Filtra todos los productos excepto el que tiene el ID dado
    productos_filtrados = list(filter(lambda producto: producto["id"] != id, productos))

    if len(productos_filtrados) == len(productos):
        return jsonify({"error": "Producto no encontrado"}), 404

    guardar_productos(productos_filtrados)
    return jsonify({"message": "Producto eliminado correctamente"}), 200


# ----------- Función para editar un producto existente -----------
def editar_producto(id):
    """
    Edita los datos de un producto identificado por ID.
    Solo se actualizan los campos enviados en el JSON de la solicitud.
    """
    productos = cargar_productos()
    data = request.get_json()

    # Busca el producto por ID
    producto_encontrado = next((producto for producto in productos if producto["id"] == id), None)

    if producto_encontrado is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Actualiza los campos si vienen en la solicitud
    producto_encontrado["nombre"] = data.get("nombre", producto_encontrado["nombre"])
    producto_encontrado["descripcion"] = data.get("descripcion", producto_encontrado["descripcion"])
    producto_encontrado["precio"] = data.get("precio", producto_encontrado["precio"])
    producto_encontrado["stock"] = data.get("stock", producto_encontrado["stock"])
    producto_encontrado["categoria"] = data.get("categoria", producto_encontrado["categoria"])

    guardar_productos(productos)
    return jsonify({"message": "Producto actualizado correctamente"}), 200

