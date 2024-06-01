from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models import Solicitud, Status, Asignacion, Grimorio
from .schemas import SolicitudCreate, SolicitudUpdate
from ..logger import logger, APIException
import random

def get_solicitud(db: Session, solicitud_id: int):
    logger.info(f"Fetching solicitud with ID {solicitud_id}")
    solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not solicitud:
        logger.warning(f"Solicitud con ID {solicitud_id} no encontrada")
        raise APIException(status_code=404, detail="Solicitud no encontrada")
    logger.info(f"Fetched solicitud: {solicitud}")
    return solicitud

def get_solicitud_by_identificacion(db: Session, identificacion: str):
    logger.info(f"Fetching solicitud with identificacion {identificacion}")
    solicitud = db.query(Solicitud).filter(Solicitud.identificacion == identificacion).first()
    if not solicitud:
        logger.warning(f"Solicitud con identificacion {identificacion} no encontrada")
    logger.info(f"Fetched solicitud: {solicitud}")
    return solicitud

def get_solicitudes(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching solicitudes with skip={skip} and limit={limit}")
    solicitudes = db.query(Solicitud).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(solicitudes)} solicitudes")
    return solicitudes

def create_solicitud(db: Session, solicitud: SolicitudCreate):
    logger.info(f"Creating new solicitud with data: {solicitud}")
    db_solicitud = Solicitud(**solicitud.dict(), status_id=1)
    try:
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        logger.info(f"Created solicitud: {db_solicitud}")
        return db_solicitud
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to create solicitud due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al crear solicitud, la identificación ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create solicitud: {e}")
        raise APIException(status_code=500, detail="Error al crear solicitud")

def update_solicitud(db: Session, solicitud_id: int, solicitud: SolicitudUpdate):
    logger.info(f"Updating solicitud with ID {solicitud_id} with data: {solicitud}")
    db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not db_solicitud:
        logger.warning(f"Solicitud con ID {solicitud_id} no encontrada")
        raise APIException(status_code=404, detail="Solicitud no encontrada")
    try:
        for key, value in solicitud.dict().items():
            setattr(db_solicitud, key, value)
        db.commit()
        db.refresh(db_solicitud)
        logger.info(f"Updated solicitud: {db_solicitud}")
        return db_solicitud
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to update solicitud due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al actualizar solicitud, datos duplicados")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update solicitud: {e}")
        raise APIException(status_code=500, detail="Error al actualizar solicitud")

def delete_solicitud(db: Session, solicitud_id: int):
    logger.info(f"Deleting solicitud with ID {solicitud_id}")
    db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not db_solicitud:
        logger.warning(f"Solicitud con ID {solicitud_id} no encontrada")
        raise APIException(status_code=404, detail="Solicitud no encontrada")
    try:
        db.delete(db_solicitud)
        db.commit()
        logger.info(f"Deleted solicitud: {db_solicitud}")
        return db_solicitud
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to delete solicitud: {e}")
        raise APIException(status_code=500, detail="Error al eliminar solicitud")

def assign_grimorio(db: Session, solicitud_id: int):
    logger.info(f"Assigning grimorio to solicitud with ID {solicitud_id}")
    db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not db_solicitud:
        logger.warning(f"Solicitud con ID {solicitud_id} no encontrada")
        raise APIException(status_code=404, detail="Solicitud no encontrada")
    try:
        grimorios = db.query(Grimorio).all()
        if not grimorios:
            logger.warning("No grimorios available")
            raise APIException(status_code=400, detail="No hay grimorios disponibles")
        
        grimorio = random.choice(grimorios)
        asignacion = Asignacion(solicitud_id=solicitud_id, grimorio_id=grimorio.id)
        db.add(asignacion)
        db.commit()
        db.refresh(asignacion)
        logger.info(f"Assigned grimorio: {asignacion}")
        return asignacion
    except APIException as e:
        db.rollback()
        logger.error(f"APIException: {e.detail}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to assign grimorio: {e}")
        raise APIException(status_code=500, detail="Error al asignar grimorio")
