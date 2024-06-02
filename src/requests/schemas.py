from typing import Optional, List
from pydantic import BaseModel, Field, validator
from ..logger import CustomValidationError
class SolicitudBase(BaseModel):
    """
    Toda búsqueda de conocimiento comienza con una solicitud,
    un humilde pedido para ser admitido en el santuario del saber.

    Atributos:
        nombre (str): Nombre del solicitante, portador de sus sueños y aspiraciones.
        apellido (str): Apellido del solicitante, vínculo con su linaje y herencia.
        identificacion (str): Identificación única del solicitante, marca de su individualidad.
        edad (int): Edad del solicitante, prueba de su madurez y preparación.
        afinidad_magica_id (int): Identificador de la afinidad mágica, conexión con su poder innato.
    """
    nombre: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$", description="El nombre debe ser un conjunto de letras.")
    apellido: str = Field(..., max_length=20, pattern="^[a-zA-Z]+$", description="El apellido debe ser un conjunto de letras.")
    identificacion: str = Field(..., max_length=10, description="La identificación debe ser única y tener un máximo de 10 caracteres.")
    edad: int = Field(..., ge=10, le=99, description="La edad debe ser un entero de dos dígitos, entre 10 y 99.")
    afinidad_magica_id: int

    @validator('nombre')
    def validar_nombre(cls, value):
        if not value:
            raise CustomValidationError(detail="No hay lugar en el mundo de la magia para alguien que no tiene nombre.")
        if not value.isalpha():
            raise CustomValidationError(detail="El nombre debe contener solo letras. Un nombre que no se ajusta a este criterio no es digno del prestigio de nuestra academia.")
        return value

    @validator('apellido')
    def validar_apellido(cls, value):
        if not value:
            raise CustomValidationError(detail="Cada aprendiz debe portar un apellido, un vínculo con su linaje.")
        if not value.isalpha():
            raise CustomValidationError(detail="El apellido debe contener solo letras. Un apellido impuro no refleja la nobleza de su portador.")
        return value

    @validator('identificacion')
    def validar_identificacion(cls, value):
        if not value:
            raise CustomValidationError(detail="Sin una identificación, un aprendiz es como un barco sin timón, perdido en la vasta mar de la magia.")
        if len(value) > 10:
            raise CustomValidationError(detail="La identificación no debe exceder los 10 caracteres. La simplicidad en la identificación es la clave de la sabiduría.")
        return value

    @validator('edad')
    def validar_edad(cls, value):
        if value < 10 or value > 99:
            raise CustomValidationError(detail="La edad debe estar entre 10 y 99 años. Solo aquellos dentro de este rango pueden aspirar a dominar las artes mágicas.")
        return value

    @validator('afinidad_magica_id')
    def validar_afinidad_magica_id(cls, value):
        if value <= 0:
            raise CustomValidationError(detail="Cada aprendiz debe poseer una afinidad mágica válida. Una afinidad incorrecta deshonra el propósito de su entrenamiento.")
        return value

class SolicitudCreate(SolicitudBase):
    """
    Crear una nueva solicitud es el primer paso en el viaje hacia el conocimiento arcano,
    un paso crucial en el sendero del aprendiz.
    """
    pass

class SolicitudUpdate(SolicitudBase):
    """
    La actualización de una solicitud es un acto de refinamiento,
    asegurando que toda la información esté en perfecta armonía.
    """
    pass

class SolicitudStatusUpdate(BaseModel):
    """
    Actualizar el estado de una solicitud es un acto de sabiduría,
    reflejando el progreso del aprendiz en su camino.

    Atributos:
        status (int): Nuevo estado de la solicitud, reflejo de su evolución.
    """
    status: int

class Asignacion(BaseModel):
    """
    La asignación de un grimorio es un momento sagrado,
    donde el poder y el conocimiento se confían a un digno aprendiz.

    Atributos:
        id (int): Identificador único de la asignación, registrado para la posteridad.
        solicitud_id (int): Identificador de la solicitud a la que se asigna el grimorio.
        grimorio_id (int): Identificador del grimorio asignado, uniendo su destino al del aprendiz.
    """
    id: int
    solicitud_id: int
    grimorio_id: int

    class Config:
        from_attributes = True

class Solicitud(SolicitudBase):
    """
    Una solicitud completa es el compendio del viaje de un aprendiz,
    reflejando su estado actual y sus asignaciones.

    Atributos:
        id (int): Identificador único de la solicitud, guardián de su historia.
        status_id (int): Estado actual de la solicitud, indicador de su progreso.
        assignments (List[Asignacion]): Lista de asignaciones de grimorios asociadas a la solicitud.
    """
    id: int
    status_id: int
    assignments: List[Asignacion] = []

    class Config:
        from_attributes = True