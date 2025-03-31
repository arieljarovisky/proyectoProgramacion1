from flask import Blueprint, request, jsonify
import os

api_blueprint = Blueprint("api", __name__)
ARCHIVO_DATOS = "datos.txt"

# Asegurar que el archivo existe
if not os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "w") as file:
        file.write("")  # Archivo vacío

@api_blueprint.route("/test", methods=["GET"])
def test():
    return "API funcionando correctamente"

@api_blueprint.route("/guardar", methods=["POST"])
def guardar():
    try:
        data = request.json  # Recibe el JSON del cuerpo del request
        with open(ARCHIVO_DATOS, "a") as file:
            file.write(f"{data}\n")  # Guarda la información en el archivo

        return jsonify({"mensaje": "Datos guardados correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
