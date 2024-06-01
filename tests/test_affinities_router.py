# tests/test_affinities_router.py
import pytest
from tests.conftest import *

def test_create_afinidad(setup_db):
    random_name = random_string()
    response = client.post("/api/afinidades/", json={"nombre": random_name})
    assert response.status_code == 200

def test_update_afinidad(setup_db):
    random_name = random_string()
    response = client.put("/api/afinidades/1", json={"nombre": random_name})
    assert response.status_code == 200
    assert response.json()["nombre"] == random_name

def test_read_afinidades(setup_db):
    response = client.get("/api/afinidades/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_afinidad(setup_db):
    response = client.get("/api/afinidades/1")
    assert response.status_code == 200
