"""
Punto de entrada principal de la aplicación Flask para Caja Plus.

- Configura la aplicación Flask.
- Habilita CORS para permitir solicitudes entre dominios (Cross-Origin Resource Sharing).
- Registra los distintos "blueprints" de rutas (módulos que agrupan endpoints por temática).
- Arranca el servidor en el puerto 5000 cuando se ejecuta este archivo directamente.

Términos clave:
- Flask: Micro-framework de Python para crear aplicaciones web y APIs.
- CORS (Cross-Origin Resource Sharing): Permite que el frontend que corre en otro origen (dominio o puerto) pueda hacer peticiones a esta API (por ejemplo, si el frontend corre en localhost:3000 y el backend en localhost:5000).
- Blueprint: Forma de organizar las rutas/endpoints de una aplicación Flask en módulos independientes. Permite mantener el código modular y ordenado, agrupando por funcionalidad (ventas, productos, usuarios, etc.).
"""

from flask import Flask
from flask_cors import CORS
from routes.api_routes import ventas_bp, productos_bp, caja_bp, pagos_bp, facturas_bp
from routes.usuarios_routes import usuarios_bp

# Inicializa la app Flask
app = Flask(__name__)

# Habilita CORS (permite llamadas desde el frontend en otros puertos/orígenes)
CORS(app)

# Registro de blueprints (modularización de rutas por funcionalidad)
app.register_blueprint(ventas_bp)       # Rutas de ventas y métricas
app.register_blueprint(usuarios_bp)     # Rutas de usuarios
app.register_blueprint(productos_bp)    # Rutas de productos
app.register_blueprint(caja_bp)         # Rutas de caja e ingresos/egresos
app.register_blueprint(pagos_bp)        # Rutas de pagos
app.register_blueprint(facturas_bp)     # Rutas de facturación

if __name__ == '__main__':
    # Ejecuta el servidor en modo debug y abierto a cualquier IP local
    app.run(host='0.0.0.0', port=5000, debug=True)
