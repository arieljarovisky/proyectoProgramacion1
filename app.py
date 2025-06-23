# Importa la clase Flask para crear la aplicación web
from flask import Flask

# Importa CORS para permitir llamadas desde otros orígenes (ej. frontend local)
from flask_cors import CORS

# Importa los blueprints definidos para las rutas de la app
from routes.api_routes import ventas_bp               # Blueprint para rutas de ventas
from routes.usuarios_routes import usuarios_bp        # Blueprint para rutas de usuarios
from routes.api_routes import ventas_bp, productos_bp, caja_bp, pagos_bp, facturas_bp
# ⚠️ Esta línea repite ventas_bp, pero también importa productos, caja, pagos y facturas


# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Habilita CORS en toda la app (necesario para permitir peticiones desde otro dominio)
CORS(app)


# Registra los diferentes blueprints (rutas) en la aplicación Flask
app.register_blueprint(ventas_bp)     # Rutas relacionadas con ventas
app.register_blueprint(usuarios_bp)   # Rutas relacionadas con usuarios
app.register_blueprint(productos_bp)  # Rutas relacionadas con productos
app.register_blueprint(caja_bp)       # Rutas relacionadas con la caja (movimientos, saldo)
app.register_blueprint(pagos_bp)      # Rutas para registrar y consultar pagos
app.register_blueprint(facturas_bp)   # Rutas para generar y descargar facturas


# Punto de entrada principal de la aplicación
# Si el archivo se ejecuta directamente, se inicia el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Corre la app en el puerto 5000 accesible desde cualquier IP

    

