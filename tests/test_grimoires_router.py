import pytest
from tests.conftest import *

def test_create_grimorio(setup_db):
    random_tipo = random_string()
    response = client.post("/api/grimorios/", json={"tipo": random_tipo, "rareza": "legendario", "peso": random_int()})
    assert response.status_code == 200

def test_update_grimorio(setup_db):
    random_tipo = random_string()
    response = client.put("/api/grimorios/1", json={"tipo": random_tipo, "rareza": "muy raro", "peso": random_int()})
    assert response.status_code == 200
    assert response.json()["tipo"] == random_tipo

def test_read_grimorio(setup_db):
    response = client.get("/api/grimorios/1")
    assert response.status_code == 200
