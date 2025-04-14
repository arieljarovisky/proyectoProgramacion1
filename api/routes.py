from flask import Blueprint, request, jsonify
import os
import json
import uuid
from datetime import datetime

api_blueprint = Blueprint("api", __name__)
ARCHIVO_COMPRAS = "database/compras.json"

# Asegurar que el archivo existe y tiene un array vacío
if not os.path.exists(ARCHIVO_COMPRAS):
    with open(ARCHIVO_COMPRAS, "w") as file:
        json.dump([], file)  # Crear un JSON con una lista vacía

@api_blueprint.route("/compras", methods=["POST"])
def registrar_compra():
    try:
        data = request.json  # Recibe el JSON del request

        # Validación básica
        if "total" not in data or "items" not in data:
            return jsonify({"error": "Faltan campos obligatorios: total e items"}), 400

        # Agregar campos adicionales
        data["id_venta"] = str(uuid.uuid4())  # ID único
        data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha actual

        # Leer datos existentes
        with open(ARCHIVO_COMPRAS, "r") as file:
            try:
                compras_existentes = json.load(file)
                if not isinstance(compras_existentes, list):
                    compras_existentes = []
            except json.JSONDecodeError:
                compras_existentes = []

        # Agregar nueva compra
        compras_existentes.append(data)

        # Guardar en el archivo
        with open(ARCHIVO_COMPRAS, "w") as file:
            json.dump(compras_existentes, file, indent=4)

        return jsonify({"mensaje": "Compra registrada correctamente", "id_venta": data["id_venta"]}), 201

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
