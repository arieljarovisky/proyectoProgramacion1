from flask import Flask
from flask_cors import CORS
from routes.api_routes import ventas_bp
from routes.usuarios_routes import usuarios_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ventas_bp)
app.register_blueprint(usuarios_bp)

# Endpoint de prueba para verificar que el servidor responde
@app.route('/api/ping')
def ping():
    return {'message': 'pong'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
