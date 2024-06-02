from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from . import service, schemas
from ..logger import logger, APIException, CustomValidationError

router = APIRouter()

@router.post("/solicitudes/", response_model=schemas.Solicitud, summary="Crear Nueva Solicitud", description="Crea una nueva solicitud con los datos proporcionados.")
def create_solicitud(solicitud: schemas.SolicitudCreate, db: Session = Depends(get_db)):
    try:
        db_solicitud = service.get_solicitud_by_identificacion(db, identificacion=solicitud.identificacion)
        if db_solicitud:
            raise APIException(status_code=400, detail="Identificación ya registrada")
        solicitud = service.create_solicitud(db=db, solicitud=solicitud)
        service.assign_grimorio(db=db, solicitud_data=solicitud)
        return solicitud
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except CustomValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.put("/solicitudes/{id}", response_model=schemas.Solicitud, summary="Actualizar Solicitud por ID", description="Actualiza los detalles de una solicitud existente por su ID.")
def update_solicitud(id: int, solicitud: schemas.SolicitudUpdate, db: Session = Depends(get_db)):
    try:
        db_solicitud = service.get_solicitud(db, solicitud_id=id)
        if not db_solicitud:
            raise APIException(status_code=404, detail="Solicitud no encontrada")
        return service.update_solicitud(db=db, solicitud_id=id, solicitud_data=solicitud)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except CustomValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.patch("/solicitudes/{id}/estatus", response_model=schemas.Solicitud, summary="Actualizar Estado de la Solicitud", description="Actualiza el estado de una solicitud existente por su ID.")
def update_solicitud_status(id: int, solicitud: schemas.SolicitudStatusUpdate, db: Session = Depends(get_db)):
    try:
        return service.update_solicitud_status(db=db, solicitud_id=id, status_id=solicitud.status_id)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except CustomValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")


@router.get("/solicitudes/", response_model=List[schemas.Solicitud], summary="Obtener todas las Solicitudes", description="Obtiene todas las solicitudes con opción de paginación.")
def read_solicitudes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return service.get_solicitudes(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

@router.delete("/solicitudes/{id}", response_model=schemas.Solicitud, summary="Eliminar Solicitud por ID", description="Elimina una solicitud existente por su ID.")
def delete_solicitud(id: int, db: Session = Depends(get_db)):
    try:
        db_solicitud = service.get_solicitud(db, solicitud_id=id)
        if not db_solicitud:
            raise APIException(status_code=404, detail="Solicitud no encontrada")
        return service.delete_solicitud(db=db, solicitud_id=id)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except CustomValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        raise HTTPException(status_code=500, detail="Error Interno del Servidor")

