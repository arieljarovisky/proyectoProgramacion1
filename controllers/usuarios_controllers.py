"""
Este módulo gestiona el CRUD de usuarios para la aplicación Caja Plus.
Incluye funciones para registrar, obtener, actualizar y eliminar usuarios,
así como para el inicio de sesión (login). La información se almacena en un
archivo JSON (`usuarios.json`) ubicado en la carpeta `data/`.

Cada función valida la entrada, manipula los datos, y devuelve una respuesta
formateada para la API.
"""

# Importa objetos de Flask para manejar peticiones y respuestas JSON
from flask import request, jsonify

# Importa librerías del sistema para manipular archivos
import json
import os

# Ruta al archivo JSON que contiene los usuarios
USUARIOS_FILE = 'data/usuarios.json'


# ----------- Función para cargar usuarios desde el archivo -----------
def cargar_usuarios():
    # Si el archivo no existe, se crea con una lista vacía
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'w') as f:
            json.dump({"usuarios": []}, f, indent=2)
        return []

    # Abre y lee el archivo, devolviendo solo la lista de usuarios
    with open(USUARIOS_FILE, 'r') as f:
        data = json.load(f)
        return data.get("usuarios", [])


# ----------- Función para guardar usuarios en el archivo -----------
def guardar_usuarios(usuarios):
    # Guarda la lista de usuarios en formato JSON, bajo la clave "usuarios"
    with open(USUARIOS_FILE, 'w') as f:
        json.dump({"usuarios": usuarios}, f, indent=2)


# ----------- Función para registrar un nuevo usuario -----------
def registrar_usuario():
    data = request.get_json()  # Extrae el JSON de la solicitud

    # Normaliza y valida los campos requeridos
    nombre = data.get('nombre', '').strip().lower()
    email = data.get('email', '').strip().lower()
    contrasena = data.get('contrasena', '').strip()

    # Verifica que todos los campos estén presentes
    if not nombre or not email or not contrasena:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Valida formato básico del email
    if '@' not in email:
        return jsonify({"error": "Email inválido"}), 400

    usuarios = cargar_usuarios()

    # Verifica que no haya otro usuario con el mismo email
    if any(u['email'] == email for u in usuarios):
        return jsonify({"error": "El email ya está registrado"}), 400

    # Genera un nuevo ID autoincremental
    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1

    # Crea el nuevo usuario
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "email": email,
        "password": contrasena
    }

    # Agrega y guarda el nuevo usuario
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    # Devuelve el usuario registrado (sin contraseña)
    return jsonify({"message": "Usuario registrado", "usuario": {
        "id": nuevo_usuario["id"],
        "nombre": nuevo_usuario["nombre"],
        "email": nuevo_usuario["email"]
    }}), 201


# ----------- Función para obtener todos los usuarios -----------
def obtener_usuarios():
    usuarios = cargar_usuarios()

    # Devuelve una lista con los datos públicos de cada usuario
    usuarios_formateados = [
        {"id": u["id"], "nombre": u["nombre"], "email": u["email"]} for u in usuarios
    ]
    return jsonify(usuarios_formateados), 200


# ----------- Función para actualizar un usuario existente -----------
def actualizar_usuario(usuario_id):
    data = request.get_json()        # Obtiene nuevos datos del usuario
    usuarios = cargar_usuarios()     # Carga los usuarios existentes

    for i in range(len(usuarios)):
        if usuarios[i]["id"] == usuario_id:
            # Actualiza los campos con nuevos valores o mantiene los actuales
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


# ----------- Función para eliminar un usuario -----------
def eliminar_usuario(usuario_id):
    usuarios = cargar_usuarios()

    # Crea una nueva lista sin el usuario a eliminar
    nuevos_usuarios = [u for u in usuarios if u["id"] != usuario_id]

    # Si la longitud no cambió, no se encontró el usuario
    if len(nuevos_usuarios) == len(usuarios):
        return jsonify({"error": "Usuario no encontrado"}), 404

    guardar_usuarios(nuevos_usuarios)
    return jsonify({"message": "Usuario eliminado"}), 200


# ----------- Función para login de usuario -----------
def login_usuario():
    data = request.get_json()  # Extrae datos del login

    # Normaliza y valida los campos
    email = data.get('email', '').strip().lower()
    contrasena = data.get('contrasena', '').strip()

    if not email or not contrasena:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if '@' not in email:
        return jsonify({"error": "Email inválido"}), 400

    usuarios = cargar_usuarios()

    # Busca usuario que coincida con email y contraseña
    for u in usuarios:
        if u["email"] == email and u["password"] == contrasena:
            return jsonify({"message": "Login exitoso", "usuario": {
                "id": u["id"],
                "nombre": u["nombre"],
                "email": u["email"],
                "rol": u.get("rol", "usuario")  # Si no tiene rol, usa "usuario" por defecto
            }}), 200

    return jsonify({"error": "Usuario no encontrado o credenciales inválidas"}), 401

