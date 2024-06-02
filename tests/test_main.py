import pytest
from random import randint
import string
import random
from tests.conftest import *

def random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def random_int(min_value=0, max_value=100):
    return randint(min_value, max_value)

@pytest.fixture(scope="module")
def create_solicitud(client):
    response = client.post("/api/solicitudes/", json={
        "nombre": "Gandalf",
        "apellido": "TheWhite",
        "identificacion": random_string(6).upper(),
        "edad": random_int(18, 60),
        "afinidad_magica_id": 1
    })
    assert response.status_code == 200
    return response.json()["id"]

def test_create_solicitud(client, setup_db):
    response = client.post("/api/solicitudes/", json={
        "nombre": "Gandalf",
        "apellido": "TheWhite",
        "identificacion": random_string(6).upper(),
        "edad": random_int(18, 60),
        "afinidad_magica_id": 1
    })
    assert response.status_code == 200

def test_read_solicitudes(client, setup_db):
    response = client.get("/api/solicitudes/")
    assert response.status_code == 200

def test_update_solicitud_status(client, setup_db, create_solicitud):
    solicitud_id = create_solicitud

    response = client.patch(f"/api/solicitudes/{solicitud_id}/estatus", json={"status_id": 1})
    assert response.status_code == 200
    assert response.json()["status_id"] == 1

def test_update_solicitud(client, setup_db, create_solicitud):
    solicitud_id = create_solicitud

    random_name = random_string()
    response = client.put(f"/api/solicitudes/{solicitud_id}", json={
        "nombre": random_name,
        "apellido": random_string(),
        "identificacion": random_string(6).upper(),
        "edad": random_int(18, 60),
        "afinidad_magica_id": 1
    })
    assert response.status_code == 200

def test_delete_solicitud(client, setup_db, create_solicitud):
    solicitud_id = create_solicitud

    response = client.delete(f"/api/solicitudes/{solicitud_id}")
    assert response.status_code == 200
