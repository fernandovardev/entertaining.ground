# src/affinities/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service

router = APIRouter()

@router.get("/afinidades/", response_model=list[schemas.AfinidadMagica])
def read_afinidades(db: Session = Depends(get_db)):
    return service.get_afinidades_magicas(db)

@router.get("/afinidades/{afinidad_id}", response_model=schemas.AfinidadMagica)
def read_afinidad(afinidad_id: int, db: Session = Depends(get_db)):
    db_afinidad = service.get_afinidad_magica(db, afinidad_id)
    if not db_afinidad:
        raise HTTPException(status_code=404, detail="Afinidad Magica not found")
    return db_afinidad

@router.post("/afinidades/", response_model=schemas.AfinidadMagica)
def create_afinidad(afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    db_afinidad = service.create_afinidad_magica(db, afinidad)
    return db_afinidad

@router.put("/afinidades/{afinidad_id}", response_model=schemas.AfinidadMagica)
def update_afinidad(afinidad_id: int, afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    db_afinidad = service.update_afinidad_magica(db, afinidad_id, afinidad)
    if not db_afinidad:
        raise HTTPException(status_code=404, detail="Afinidad Magica not found")
    return db_afinidad
