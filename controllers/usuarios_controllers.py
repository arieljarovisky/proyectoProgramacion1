from flask import request, jsonify
import json
import os

USUARIOS_FILE = 'data/usuarios.json'

# Cargar usuarios
def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'w') as f:
            json.dump([], f)
        return []

    with open(USUARIOS_FILE, 'r') as f:
        return json.load(f)

# Guardar usuarios
def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=2)

# Registrar un nuevo usuario
def registrar_usuario():
    data = request.get_json()

    nombre = data.get('nombre', '').strip().lower()
    email = data.get('email', '').strip().lower()
    password = data.get('contrasena', '').strip()

    if not nombre or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if '@' not in email:
        return jsonify({"error": "Email inválido"}), 400

    usuarios = cargar_usuarios()

    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "email": email,
        "contraseña": password  # En producción, se debe hashear
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return jsonify({"message": "Usuario registrado", "usuario": nuevo_usuario}), 201

# Obtener todos los usuarios
def obtener_usuarios():
    usuarios = cargar_usuarios()
    return jsonify(usuarios), 200

# Actualizar usuario
def actualizar_usuario(usuario_id):
    data = request.get_json()
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["id"] == usuario_id:
            u["nombre"] = data.get("nombre", u["nombre"]).strip().lower()
            u["email"] = data.get("email", u["email"]).strip().lower()
            u["contraseña"] = data.get("contraseña", u["contraseña"]).strip()
            guardar_usuarios(usuarios)
            return jsonify({"message": "Usuario actualizado", "usuario": u}), 200

    return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar usuario
def eliminar_usuario(usuario_id):
    usuarios = cargar_usuarios()
    usuarios_filtrados = [u for u in usuarios if u["id"] != usuario_id]

    if len(usuarios_filtrados) == len(usuarios):
        return jsonify({"error": "Usuario no encontrado"}), 404

    guardar_usuarios(usuarios_filtrados)
    return jsonify({"message": "Usuario eliminado"}), 200

# Login de usuario
def login_usuario():
    data = request.get_json()

    email = data.get('email', '').strip().lower()
    contrasena = data.get('contrasena', '').strip()

    if not email or not contrasena:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if '@' not in email:
        return jsonify({"error": "Email inválido"}), 400

    usuarios = cargar_usuarios()
    for u in usuarios:
        if u["email"] == email and u["contrasena"] == contrasena:
            return jsonify({"message": "Login exitoso", "usuario": u}), 200

    return jsonify({"error": "Usuario no encontrado o credenciales inválidas"}), 401

