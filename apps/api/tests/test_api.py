from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_templates():
    response = client.get('/templates')
    assert response.status_code == 200
    assert any(item['id'] == 'fastapi-api' for item in response.json())


def test_generate():
    response = client.post('/generate', json={
        'name': 'demo-app',
        'template': 'fastapi-api',
        'description': 'A demo API'
    })
    assert response.status_code == 200
    assert response.json()['status'] == 'completed'
