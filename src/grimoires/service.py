from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models import *
from .schemas import GrimorioCreate
from ..logger import logger, APIException


def get_grimorios(db: Session):
    logger.info("Fetching all grimorios from database")
    try:
        grimorios = db.query(Grimorio).all()
        grimorios = [grimorio.serialize() for grimorio in grimorios]
        logger.info(f"Fetched {len(grimorios)} grimorios")
        return grimorios
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener grimorios: {e}")
        raise APIException(status_code=500, detail="Error al obtener grimorios")

def get_grimorio(db: Session, grimorio_id: int):
    logger.info(f"Fetching grimorio with ID {grimorio_id}")
    try:
        grimorio = db.query(Grimorio).filter(Grimorio.id == grimorio_id).first()
        if not grimorio:
            logger.warning(f"Grimorio con ID {grimorio_id} no encontrado")
            raise APIException(status_code=404, detail="Grimorio no encontrado")
        logger.info(f"Fetched grimorio: {grimorio.serialize()}")
        return grimorio.serialize()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener grimorio con ID {grimorio_id}: {e}")
        raise APIException(status_code=500, detail="Error al obtener grimorio")

def create_grimorio(db: Session, grimorio: GrimorioCreate):
    logger.info(f"Creating new grimorio with data: {grimorio}")
    db_grimorio = Grimorio(**grimorio.dict())
    try:
        db.add(db_grimorio)
        db.commit()
        db.refresh(db_grimorio)
        logger.info(f"Created grimorio: {db_grimorio.serialize()}")
        return db_grimorio.serialize()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to create grimorio due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al crear grimorio, el grimorio ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create grimorio: {e}")
        raise APIException(status_code=500, detail="Error al crear grimorio")

def update_grimorio(db: Session, grimorio_id: int, grimorio_data: GrimorioCreate):
    logger.info(f"Updating grimorio with ID {grimorio_id} with data: {grimorio_data}")
    try:
        grimorio = db.query(Grimorio).filter(Grimorio.id == grimorio_id).first()
        if not grimorio:
            logger.warning(f"Grimorio con ID {grimorio_id} no encontrado")
            raise APIException(status_code=404, detail="Grimorio no encontrado")

        for key, value in grimorio_data.dict().items():
            setattr(grimorio, key, value)

        db.commit()
        db.refresh(grimorio)
        logger.info(f"Updated grimorio: {grimorio.serialize()}")
        return grimorio.serialize()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to update grimorio due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al actualizar grimorio, datos duplicados")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update grimorio: {e}")
        raise APIException(status_code=500, detail="Error al actualizar grimorio")

def get_grimorio_by_solicitud_id(db: Session, solicitud_id: int):
    logger.info(f"Fetching grimorio for solicitud ID {solicitud_id}")
    asignacion = db.query(Asignacion).filter(Asignacion.solicitud_id == solicitud_id).first()
    if not asignacion:
        logger.warning(f"No grimorio found for solicitud ID {solicitud_id}")
        raise APIException(status_code=404, detail="Grimorio no encontrado")
    grimorio = db.query(Grimorio).filter(Grimorio.id == asignacion.grimorio_id).first()
    logger.info(f"Fetched grimorio: {grimorio.serialize()}")
    return grimorio.serialize()