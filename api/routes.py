from flask import Blueprint, request, jsonify
import os
import json

api_blueprint = Blueprint("api", __name__)
ARCHIVO_DATOS = "database/datos.json"

# Asegurar que el archivo existe y tiene un array vacío
if not os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "w") as file:
        json.dump([], file)  # Crear un JSON con una lista vacía

@api_blueprint.route("/test", methods=["GET"])
def test():
    return "API funcionando correctamente"

@api_blueprint.route("/guardar", methods=["POST"])
def guardar():
    try:
        data = request.json  # Recibe el JSON del request
        
        # Leer datos existentes
        with open(ARCHIVO_DATOS, "r") as file:
            try:
                datos_existentes = json.load(file)  # Cargar JSON
                if not isinstance(datos_existentes, list):  
                    datos_existentes = []  # Si no es una lista, reiniciar
            except json.JSONDecodeError:
                datos_existentes = []  # Si hay un error, reiniciar

        # Agregar nuevo dato
        datos_existentes.append(data)

        # Guardar en el archivo
        with open(ARCHIVO_DATOS, "w") as file:
            json.dump(datos_existentes, file, indent=4)

        return jsonify({"mensaje": "Datos guardados correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_blueprint.route("/login", methods=["POST"])
def login():
    ARCHIVO_USUARIOS = "database/usuarios.json"

    try:
        datos = request.json  # Recibe JSON con email y contrasena

        # Verificar que vengan los campos necesarios
        if "email" not in datos or "contrasena" not in datos:
            return jsonify({"error": "Faltan campos obligatorios: email y contrasena"}), 400

        # Leer usuarios
        if not os.path.exists(ARCHIVO_USUARIOS):
            return jsonify({"error": "No hay usuarios registrados"}), 404

        with open(ARCHIVO_USUARIOS, "r") as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []

        # Buscar el usuario por email
        usuario = next((u for u in usuarios if u.get("email") == datos["email"]), None)

        if usuario is None:
            return jsonify({"error": "Email no registrado"}), 404

        # Comparar contraseñas
        if usuario.get("contrasena") != datos["contrasena"]:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        return jsonify({"mensaje": "Login exitoso", "usuario": usuario}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
