from pydantic import BaseModel

class AfinidadMagicaBase(BaseModel):
    nombre: str

class AfinidadMagicaCreate(AfinidadMagicaBase):
    pass

class AfinidadMagica(AfinidadMagicaBase):
    id: int

    class Config:
        from_attributes = True
