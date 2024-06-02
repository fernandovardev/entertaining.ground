from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service
from ..logger import logger, APIException

router = APIRouter()

@router.get("/grimorios/", response_model=list[schemas.Grimorio], summary="Obtener todos los Grimorios", description="Obtiene todos los grimorios disponibles en la base de datos.")
def read_grimorios(db: Session = Depends(get_db)):
    logger.info("Solicitud para obtener todos los grimorios")
    try:
        return service.get_grimorios(db)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.get("/grimorios/{grimorio_id}", response_model=schemas.Grimorio, summary="Obtener Grimorio por ID", description="Obtiene un grimorio por su ID único.")
def read_grimorio(grimorio_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener grimorio con ID {grimorio_id}")
    try:
        db_grimorio = service.get_grimorio(db, grimorio_id)
        if not db_grimorio:
            logger.warning(f"Grimorio con ID {grimorio_id} no encontrado")
            raise APIException(status_code=404, detail="Grimorio no encontrado")
        return db_grimorio
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.post("/grimorios/", response_model=schemas.Grimorio, summary="Crear Nuevo Grimorio", description="Crea un nuevo grimorio con los datos proporcionados.")
def create_grimorio(grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear grimorio con datos: {grimorio}")
    try:
        return service.create_grimorio(db, grimorio)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.put("/grimorios/{grimorio_id}", response_model=schemas.Grimorio, summary="Actualizar Grimorio por ID", description="Actualiza los detalles de un grimorio existente por su ID.")
def update_grimorio(grimorio_id: int, grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar grimorio con ID {grimorio_id} con datos: {grimorio}")
    try:
        return service.update_grimorio(db, grimorio_id, grimorio)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")
