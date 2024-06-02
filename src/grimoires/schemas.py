from pydantic import BaseModel

class GrimorioBase(BaseModel):
    """
    Los grimorios son recipientes de conocimiento y poder,
    esenciales para cualquier mago que aspire a la grandeza.

    Atributos:
        tipo (str): El tipo de grimorio, que determina su uso y aplicaciones.
        rareza (str): La rareza del grimorio, indicador de su valor y poder.
        peso (int): El peso del grimorio, símbolo de su contenido y capacidad.
    """
    tipo: str
    rareza: str
    peso: int

class GrimorioCreate(GrimorioBase):
    """
    Crear un nuevo grimorio es como forjar un arma de sabiduría y poder,
    lista para ser empuñada por aquellos dignos de su contenido.
    """
    pass

class Grimorio(GrimorioBase):
    """
    Cada grimorio debe ser único, conocido por su nombre y registro,
    para asegurar que su conocimiento no se pierda en las brumas del tiempo.

    Atributos:
        id (int): Identificador único del grimorio, preservando su legado.
    """
    id: int

    class Config:
        from_attributes = True

