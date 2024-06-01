from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
Base = declarative_base()

class StatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), index=True)
    apellido = Column(String(20), index=True)
    identificacion = Column(String(10), unique=True, index=True)
    edad = Column(Integer)
    afinidad_magica_id = Column(Integer, ForeignKey('afinidades_magicas.id'))
    status = Column(SAEnum(StatusEnum), default=StatusEnum.PENDING)

    afinidad_magica = relationship("AfinidadMagica")
    assignments = relationship("Asignacion", back_populates="solicitud")


class AfinidadMagica(Base):
    __tablename__ = "afinidades_magicas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), unique=True, index=True)

class Grimorio(Base):
    __tablename__ = "grimorios"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), unique=True, index=True)
    rareza = Column(String(20))
    peso = Column(Integer)


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey('solicitudes.id'))
    grimorio_id = Column(Integer, ForeignKey('grimorios.id'))

    solicitud = relationship("Solicitud", back_populates="assignments")
    grimorio = relationship("Grimorio")
