from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service
from ..logger import logger, APIException

router = APIRouter()

@router.get("/afinidades/", response_model=list[schemas.AfinidadMagica], summary="Obtener todas las Afinidades Mágicas", description="Obtiene todas las afinidades mágicas disponibles en la base de datos.")
def read_afinidades(db: Session = Depends(get_db)):
    logger.info("Solicitud para obtener todas las afinidades mágicas")
    try:
        return service.get_afinidades_magicas(db)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.get("/afinidades/{afinidad_id}", response_model=schemas.AfinidadMagica, summary="Obtener Afinidad Mágica por ID", description="Obtiene una afinidad mágica por su ID único.")
def read_afinidad(afinidad_id: int, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para obtener afinidad mágica con ID {afinidad_id}")
    try:
        db_afinidad = service.get_afinidad_magica(db, afinidad_id)
        if not db_afinidad:
            logger.warning(f"Afinidad mágica con ID {afinidad_id} no encontrada")
            raise APIException(status_code=404, detail="Afinidad Mágica no encontrada")
        return db_afinidad
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.post("/afinidades/", response_model=schemas.AfinidadMagica, summary="Crear Nueva Afinidad Mágica", description="Crea una nueva afinidad mágica con los datos proporcionados.")
def create_afinidad(afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para crear afinidad con datos: {afinidad}")
    try:
        return service.create_afinidad_magica(db, afinidad)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.put("/afinidades/{afinidad_id}", response_model=schemas.AfinidadUpdate, summary="Actualizar Afinidad Mágica por ID", description="Actualiza los detalles de una afinidad mágica existente por su ID.")
def update_afinidad(afinidad_id: int, afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitud para actualizar afinidad mágica con ID {afinidad_id} con datos: {afinidad}")
    try:
        return service.update_afinidad_magica(db, afinidad_id, afinidad)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")
