"""
Este archivo representa el punto de entrada principal del backend de la aplicación Caja Plus.
Configura la app de Flask, habilita CORS para permitir comunicación con el frontend,
e importa y registra los blueprints que agrupan las rutas de distintas funcionalidades:
ventas, usuarios, productos, caja, pagos y facturación.

El archivo se encarga de:
- Inicializar la app.
- Habilitar CORS (Cross-Origin Resource Sharing).
- Registrar las rutas organizadas en módulos (blueprints).
- Ejecutar el servidor Flask si el archivo es corrido directamente.
"""

# Importa la clase Flask para crear la aplicación web
from flask import Flask

# Importa CORS para permitir llamadas desde otros orígenes (ej. frontend local)
from flask_cors import CORS

# Importa blueprints para las rutas organizadas del sistema
from routes.api_routes import ventas_bp               # Blueprint para rutas de ventas
from routes.usuarios_routes import usuarios_bp        # Blueprint para rutas de usuarios
from routes.api_routes import ventas_bp, productos_bp, caja_bp, pagos_bp, facturas_bp
# ⚠️ Esta línea repite ventas_bp (ya importado antes), pero también importa productos_bp, caja_bp, pagos_bp y facturas_bp

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Habilita CORS en toda la app (necesario para permitir peticiones desde un frontend distinto al backend)
CORS(app)

# Registra los diferentes blueprints (rutas) en la aplicación Flask
app.register_blueprint(ventas_bp)     # Rutas relacionadas con ventas
app.register_blueprint(usuarios_bp)   # Rutas relacionadas con usuarios
app.register_blueprint(productos_bp)  # Rutas relacionadas con productos
app.register_blueprint(caja_bp)       # Rutas relacionadas con caja (ingresos, egresos, saldo)
app.register_blueprint(pagos_bp)      # Rutas relacionadas con pagos
app.register_blueprint(facturas_bp)   # Rutas relacionadas con generación y descarga de facturas

# Punto de entrada principal de la aplicación
# Si el archivo se ejecuta directamente (no importado como módulo), arranca el servidor en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Ejecuta la app en el puerto 5000, accesible desde cualquier IP

    

