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
    contrasena = data.get('contrasena', '').strip()

    if not nombre or not email or not contrasena:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if '@' not in email:
        return jsonify({"error": "Email inválido"}), 400

    usuarios = cargar_usuarios()

    nuevo_usuario = [
        len(usuarios) + 1,  # ID
        nombre,
        email,
        contrasena
    ]

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return jsonify({"message": "Usuario registrado", "usuario": {
        "id": nuevo_usuario[0],
        "nombre": nuevo_usuario[1],
        "email": nuevo_usuario[2]
    }}), 201

# Obtener todos los usuarios
def obtener_usuarios():
    usuarios = cargar_usuarios()
    usuarios_formateados = [
        {"id": u[0], "nombre": u[1], "email": u[2]} for u in usuarios
    ]
    return jsonify(usuarios_formateados), 200

# Actualizar usuario
def actualizar_usuario(usuario_id):
    data = request.get_json()
    usuarios = cargar_usuarios()

    for i in range(len(usuarios)):
        if usuarios[i][0] == usuario_id:
            usuarios[i][1] = data.get("nombre", usuarios[i][1]).strip().lower()
            usuarios[i][2] = data.get("email", usuarios[i][2]).strip().lower()
            usuarios[i][3] = data.get("contrasena", usuarios[i][3]).strip()
            guardar_usuarios(usuarios)
            return jsonify({"message": "Usuario actualizado", "usuario": {
                "id": usuarios[i][0],
                "nombre": usuarios[i][1],
                "email": usuarios[i][2]
            }}), 200

    return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar usuario
def eliminar_usuario(usuario_id):
    usuarios = cargar_usuarios()
    usuarios_filtrados = [u for u in usuarios if u[0] != usuario_id]

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
        if u[2] == email and u[3] == contrasena:
            return jsonify({"message": "Login exitoso", "usuario": {
                "id": u[0],
                "nombre": u[1],
                "email": u[2]
            }}), 200

    return jsonify({"error": "Usuario no encontrado o credenciales inválidas"}), 401
