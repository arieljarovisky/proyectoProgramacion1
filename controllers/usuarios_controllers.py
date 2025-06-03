from flask import request, jsonify
import json
import os

USUARIOS_FILE = 'data/usuarios.json'

# Cargar usuarios
def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'w') as f:
            json.dump({"usuarios": []}, f, indent=2)
        return []

    with open(USUARIOS_FILE, 'r') as f:
        data = json.load(f)
        return data.get("usuarios", [])

# Guardar usuarios
def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump({"usuarios": usuarios}, f, indent=2)

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

    # Verificar si ya existe ese email
    if any(u['email'] == email for u in usuarios):
        return jsonify({"error": "El email ya está registrado"}), 400

    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "email": email,
        "password": contrasena
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return jsonify({"message": "Usuario registrado", "usuario": {
        "id": nuevo_usuario["id"],
        "nombre": nuevo_usuario["nombre"],
        "email": nuevo_usuario["email"]
    }}), 201

# Obtener todos los usuarios
def obtener_usuarios():
    usuarios = cargar_usuarios()
    usuarios_formateados = [
        {"id": u["id"], "nombre": u["nombre"], "email": u["email"]} for u in usuarios
    ]
    return jsonify(usuarios_formateados), 200

# Actualizar usuario
def actualizar_usuario(usuario_id):
    data = request.get_json()
    usuarios = cargar_usuarios()

    for i in range(len(usuarios)):
        if usuarios[i]["id"] == usuario_id:
            usuarios[i]["nombre"] = data.get("nombre", usuarios[i]["nombre"]).strip().lower()
            usuarios[i]["email"] = data.get("email", usuarios[i]["email"]).strip().lower()
            usuarios[i]["password"] = data.get("contrasena", usuarios[i]["password"]).strip()
            guardar_usuarios(usuarios)
            return jsonify({"message": "Usuario actualizado", "usuario": {
                "id": usuarios[i]["id"],
                "nombre": usuarios[i]["nombre"],
                "email": usuarios[i]["email"]
            }}), 200

    return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar usuario
def eliminar_usuario(usuario_id):
    usuarios = cargar_usuarios()
    nuevos_usuarios = [u for u in usuarios if u["id"] != usuario_id]

    if len(nuevos_usuarios) == len(usuarios):
        return jsonify({"error": "Usuario no encontrado"}), 404

    guardar_usuarios(nuevos_usuarios)
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
        if u["email"] == email and u["password"] == contrasena:
            return jsonify({"message": "Login exitoso", "usuario": {
                "id": u["id"],
                "nombre": u["nombre"],
                "email": u["email"],
                "rol": u["rol"]
            }}), 200

    return jsonify({"error": "Usuario no encontrado o credenciales inválidas"}), 401
