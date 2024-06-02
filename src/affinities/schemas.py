from pydantic import BaseModel, Field
from typing import Optional
class AfinidadMagicaBase(BaseModel):
    """
    En el vasto océano de la magia, cada mago debe tener una afinidad,
    una conexión intrínseca con un tipo de energía arcana.
    
    Atributos:
        nombre (str): El nombre de la afinidad mágica, un reflejo de su esencia.
    """
    id: Optional[int] = Field(None, description="The unique identifier of the afinidad")
    nombre: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Fuego"
            }
        }

class AfinidadMagicaCreate(AfinidadMagicaBase):
    """
    Cuando un nuevo aprendiz es admitido en nuestras sagradas filas,
    se debe registrar su afinidad mágica para poder guiar su entrenamiento.
    """
    pass

class AfinidadMagica(AfinidadMagicaBase):
    """
    Así como las estrellas tienen nombres y lugares en el firmamento,
    cada afinidad mágica debe ser única y estar claramente identificada.

    Atributos:
        id (int): Identificador único de la afinidad mágica, grabado en los anales de nuestra academia.
    """
    id: int

    class Config:
        from_attributes = True

class AfinidadUpdate(BaseModel):
    nombre: str
    id: Optional[int] = Field(None, description="The unique identifier of the afinidad")