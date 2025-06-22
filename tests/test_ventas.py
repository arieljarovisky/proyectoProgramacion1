import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture que configura el test client de Flask en modo TESTING.
    """
    app.config["TESTING"] = True
    return app.test_client()

def test_obtener_ventas_devuelve_lista(client):
    """
    Esta funcion verifica que el endpoint GET /api/ventas:
    - Responda con HTTP 200.
    - Devuelva siempre un JSON de tipo lista (puede estar vacío o no).
    """
    resp = client.get("/api/ventas")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_registrar_venta_sin_items(client):
    """
    Esta funcion verifica que el endpoint POST /api/ventas/compras:
    - Al recibir una lista de items vacía responda con HTTP 400.
    - Incluya en el JSON un campo "error" describiendo el problema.
    """
    resp = client.post("/api/ventas/compras", json={"items": []})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
