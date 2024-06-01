from pydantic import BaseModel

class GrimorioBase(BaseModel):
    tipo: str
    rareza: str
    peso: int

class GrimorioCreate(GrimorioBase):
    pass

class Grimorio(GrimorioBase):
    id: int

    class Config:
        orm_mode = True
