import os
from flask import Flask
from flask_cors import CORS
from api.routes import api_blueprint
from database.database import inicializar_archivo

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todas las rutas

    # Inicializar la base de datos (archivos)
    inicializar_archivo()

    # Registrar las rutas de la API
    app.register_blueprint(api_blueprint)

    return app

if __name__ == "__main__":
    # Ejecutar la aplicación en modo debug
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
