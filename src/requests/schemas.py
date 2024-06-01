from pydantic import BaseModel, Field
from typing import Optional, List

class SolicitudBase(BaseModel):
    nombre: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$")
    apellido: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$")
    identificacion: str = Field(..., max_length=10)
    edad: int = Field(..., ge=10, le=99)
    afinidad_magica_id: int

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(SolicitudBase):
    pass

class SolicitudStatusUpdate(BaseModel):
    status: str

class Solicitud(SolicitudBase):
    id: int
    status: str
    assignments: List['Asignacion']

    class Config:
        orm_mode = True

class AsignacionBase(BaseModel):
    solicitud_id: int
    grimorio_id: int

class Asignacion(AsignacionBase):
    id: int

    class Config:
        orm_mode = True
