import pytest
from tests.conftest import *

def test_create_solicitud(setup_db):
    response = client.post("/api/solicitudes/", json={
        "nombre": "Gandalf",
        "apellido": "TheWhite",
        "identificacion": random_string(6).upper(),
        "edad": random_int(18, 60),
        "afinidad_magica_id": 1
    })
    assert response.status_code == 201
#
#def test_read_solicitudes(setup_db):
#    response = client.get("/api/solicitudes/")
#    assert response.status_code == 200
#
#def test_update_solicitud_status(setup_db):
#    response = client.patch("/api/solicitudes/1/estatus", json={"status": "approved"})
#    assert response.status_code == 200
#
#def test_update_solicitud(setup_db):
#    random_name = random_string()
#    response = client.put("/api/solicitudes/1", json={
#        "nombre": random_name,
#        "apellido": random_string(),
#        "identificacion": random_string(6).upper(),
#        "edad": random_int(18, 60),
#        "afinidad_magica_id": 1
#    })
#    assert response.status_code == 200
#
#def test_delete_solicitud(setup_db):
#    response = client.delete("/api/solicitudes/1")
#    assert response.status_code == 200
