# Importa el módulo pytest, utilizado para realizar pruebas unitarias
import pytest

# Importa la instancia de la aplicación Flask desde el módulo principal
from app import app

# ---------- FIXTURE ----------

@pytest.fixture
def client():
    """
    Crea un cliente de pruebas para simular peticiones HTTP a la app Flask.
    Activa el modo TESTING, que desactiva ciertas funcionalidades (como errores reales).
    """
    app.config["TESTING"] = True  # Configura la app en modo testing
    return app.test_client()      # Retorna el cliente de prueba

# ---------- TEST 1 ----------

def test_obtener_ventas_devuelve_lista(client):
    """
    Prueba que el endpoint GET /api/ventas:
    - Devuelva código HTTP 200 (OK).
    - Devuelva un JSON con formato de lista (aunque esté vacía).
    """
    resp = client.get("/api/ventas")     # Se hace la petición GET al endpoint de ventas
    assert resp.status_code == 200       # Se espera un status 200 OK
    data = resp.get_json()               # Se obtiene la respuesta en formato JSON
    assert isinstance(data, list)        # Se verifica que la respuesta sea una lista

# ---------- TEST 2 ----------

def test_registrar_venta_sin_items(client):
    """
    Prueba que el endpoint POST /api/ventas/compras:
    - Devuelva HTTP 400 si se intenta registrar una venta sin items.
    - Incluya un mensaje de error en el JSON de respuesta.
    """
    resp = client.post("/api/ventas/compras", json={"items": []})  # Envía una lista vacía
    assert resp.status_code == 400         # Se espera error 400
    data = resp.get_json()                 # Se obtiene la respuesta
    assert "error" in data                 # Se verifica que exista un mensaje de error
