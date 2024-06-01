from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from . import service, schemas

router = APIRouter()

@router.post("/solicitudes/", response_model=schemas.Solicitud)
def create_solicitud(solicitud: schemas.SolicitudCreate, db: Session = Depends(get_db)):
    db_solicitud = service.get_solicitud_by_identificacion(db, identificacion=solicitud.identificacion)
    if db_solicitud:
        raise HTTPException(status_code=400, detail="Identificación ya registrada")
    solicitud = service.create_solicitud(db=db, solicitud=solicitud)
    service.assign_grimorio(db=db, solicitud_id=solicitud.id)
    return solicitud

@router.put("/solicitudes/{id}", response_model=schemas.Solicitud)
def update_solicitud(id: int, solicitud: schemas.SolicitudUpdate, db: Session = Depends(get_db)):
    db_solicitud = service.get_solicitud(db, solicitud_id=id)
    if not db_solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return service.update_solicitud(db=db, solicitud_id=id, solicitud=solicitud)

@router.patch("/solicitudes/{id}/estatus", response_model=schemas.Solicitud)
def update_solicitud_status(id: int, solicitud: schemas.SolicitudStatusUpdate, db: Session = Depends(get_db)):
    db_solicitud = service.get_solicitud(db, solicitud_id=id)
    if not db_solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    db_solicitud.status = solicitud.status
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud

@router.get("/solicitudes/", response_model=List[schemas.Solicitud])
def read_solicitudes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    solicitudes = service.get_solicitudes(db, skip=skip, limit=limit)
    return solicitudes

@router.delete("/solicitudes/{id}", response_model=schemas.Solicitud)
def delete_solicitud(id: int, db: Session = Depends(get_db)):
    db_solicitud = service.get_solicitud(db, solicitud_id=id)
    if not db_solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    service.delete_solicitud(db=db, solicitud_id=id)
    return db_solicitud

