# src/affinities/service.py
from sqlalchemy.orm import Session
from ..models import AfinidadMagica
from .schemas import AfinidadMagicaCreate, AfinidadMagica as AfinidadMagicaSchema

def get_afinidades_magicas(db: Session):
    return db.query(AfinidadMagica).all()

def get_afinidad_magica(db: Session, afinidad_id: int):
    return db.query(AfinidadMagica).filter(AfinidadMagica.id == afinidad_id).first()

def create_afinidad_magica(db: Session, afinidad: AfinidadMagicaCreate):
    db_afinidad = AfinidadMagica(**afinidad.dict())
    db.add(db_afinidad)
    db.commit()
    db.refresh(db_afinidad)
    return db_afinidad

def update_afinidad_magica(db: Session, afinidad_id: int, afinidad_data: AfinidadMagicaCreate):
    afinidad = db.query(AfinidadMagica).filter(AfinidadMagica.id == afinidad_id).first()
    if afinidad:
        for key, value in afinidad_data.dict().items():
            setattr(afinidad, key, value)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(afinidad)
    return afinidad
