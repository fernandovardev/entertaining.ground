from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from src.database import engine

Base = declarative_base()

class Status(Base):
    __tablename__ = "status"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), index=True)
    apellido = Column(String(20), index=True)
    identificacion = Column(String(10), unique=True, index=True)
    edad = Column(Integer)
    afinidad_magica_id = Column(Integer, ForeignKey('afinidades_magicas.id'))
    status_id = Column(Integer, ForeignKey('status.id'))

    afinidad_magica = relationship("AfinidadMagica")
    status = relationship("Status")
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
Base.metadata.create_all(bind=engine)
