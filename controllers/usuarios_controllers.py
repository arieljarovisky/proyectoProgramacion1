"""
Controlador para el manejo CRUD y autenticación de usuarios en el sistema.

Conceptos clave:
- CRUD: Crear, Leer, Actualizar, Eliminar.
- Autenticación: Verifica si el usuario y contraseña existen en la base.
- JSON: Se usa como base de datos ligera para almacenar usuarios.

Notas de seguridad:
- En este proyecto las contraseñas se almacenan en texto plano ya que es solo con propósitos educativos.
- **NUNCA** almacenar contraseñas en texto plano en producción. Usar SIEMPRE  un hash seguro como bcrypt o similar.
"""

from flask import request, jsonify
import json
import os

# Ruta al archivo donde se almacenan los usuarios en formato JSON
USUARIOS_FILE = 'data/usuarios.json'

def cargar_usuarios():
    """
    Carga la lista de usuarios desde el archivo JSON.
    Si no existe, lo crea con una lista vacía.

    Returns:
        list: Lista de usuarios (cada uno es un dict).
    """
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'w') as f:
            json.dump({"usuarios": []}, f, indent=2)
        return []

    with open(USUARIOS_FILE, 'r') as f:
        data = json.load(f)
        return data.get("usuarios", [])

def guardar_usuarios(usuarios):
    """
    Guarda la lista de usuarios en el archivo JSON.

    Args:
        usuarios (list): Lista de usuarios.
    """
    with open(USUARIOS_FILE, 'w') as f:
        json.dump({"usuarios": usuarios}, f, indent=2)

def registrar_usuario():
    """
    Endpoint para registrar un nuevo usuario.

    Validaciones:
    - Nombre, email y contraseña no vacíos.
    - Email debe tener '@'.
    - Email no repetido en la base.

    Returns:
        Response: Mensaje de éxito y usuario creado, o error.
    """
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
        "password": contrasena,
        # "rol": "admin"  # <- Podrías agregar rol por defecto si lo necesitás
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return jsonify({"message": "Usuario registrado", "usuario": {
        "id": nuevo_usuario["id"],
        "nombre": nuevo_usuario["nombre"],
        "email": nuevo_usuario["email"]
    }}), 201

def obtener_usuarios():
    """
    Endpoint para obtener todos los usuarios registrados.

    Returns:
        Response: Lista de usuarios (sin password), código 200.
    """
    usuarios = cargar_usuarios()
    usuarios_formateados = [
        {"id": u["id"], "nombre": u["nombre"], "email": u["email"]} for u in usuarios
    ]
    return jsonify(usuarios_formateados), 200

def actualizar_usuario(usuario_id):
    """
    Endpoint para actualizar los datos de un usuario por ID.

    Args:
        usuario_id (int): ID del usuario a actualizar.

    Returns:
        Response: Usuario actualizado o mensaje de error.
    """
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

def eliminar_usuario(usuario_id):
    """
    Endpoint para eliminar un usuario por ID.

    Args:
        usuario_id (int): ID del usuario a eliminar.

    Returns:
        Response: Mensaje de éxito o error si no lo encuentra.
    """
    usuarios = cargar_usuarios()
    nuevos_usuarios = [u for u in usuarios if u["id"] != usuario_id]

    if len(nuevos_usuarios) == len(usuarios):
        return jsonify({"error": "Usuario no encontrado"}), 404

    guardar_usuarios(nuevos_usuarios)
    return jsonify({"message": "Usuario eliminado"}), 200

def login_usuario():
    """
    Endpoint de login (autenticación de usuario).

    Validaciones:
    - Email y contraseña no vacíos.
    - Email debe contener '@'.
    - Compara email y contraseña contra los datos guardados.

    Returns:
        Response: Mensaje de login exitoso (y datos del usuario, excepto contraseña) o error.
    """
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
            # Incluí el campo "rol" si lo tuvieras en la estructura de usuario.
            return jsonify({"message": "Login exitoso", "usuario": {
                "id": u["id"],
                "nombre": u["nombre"],
                "email": u["email"],
                "rol": u.get("rol", "admin")  # Valor por defecto si no está el campo.
            }}), 200

    return jsonify({"error": "Usuario no encontrado o credenciales inválidas"}), 401
