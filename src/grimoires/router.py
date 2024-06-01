# src/grimoires/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service

router = APIRouter()

@router.get("/grimorios/", response_model=list[schemas.Grimorio])
def read_grimorios(db: Session = Depends(get_db)):
    return service.get_grimorios(db)

@router.get("/grimorios/{grimorio_id}", response_model=schemas.Grimorio)
def read_grimorio(grimorio_id: int, db: Session = Depends(get_db)):
    db_grimorio = service.get_grimorio(db, grimorio_id)
    if not db_grimorio:
        raise HTTPException(status_code=404, detail="Grimorio not found")
    return db_grimorio

@router.post("/grimorios/", response_model=schemas.Grimorio)
def create_grimorio(grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    db_grimorio = service.create_grimorio(db, grimorio)
    return db_grimorio

@router.put("/grimorios/{grimorio_id}", response_model=schemas.Grimorio)
def update_grimorio(grimorio_id: int, grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    db_grimorio = service.update_grimorio(db, grimorio_id, grimorio)
    if not db_grimorio:
        raise HTTPException(status_code=404, detail="Grimorio not found")
    return db_grimorio
