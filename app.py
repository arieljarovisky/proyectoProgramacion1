from flask import Flask
from flask_cors import CORS
from routes.api_routes import ventas_bp
from routes.usuarios_routes import usuarios_bp
from routes.api_routes import ventas_bp, productos_bp, caja_bp, pagos_bp, facturas_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ventas_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(caja_bp)
app.register_blueprint(pagos_bp)
app.register_blueprint(facturas_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    

