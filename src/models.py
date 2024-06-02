from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Status(Base):
    __tablename__ = "status"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    
    solicitudes = relationship("Solicitud", back_populates="status")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), index=True)
    apellido = Column(String(20), index=True)
    identificacion = Column(String(10), unique=True, index=True)
    edad = Column(Integer)
    afinidad_magica_id = Column(Integer, ForeignKey('afinidades_magicas.id'))
    status_id = Column(Integer, ForeignKey('status.id'))

    afinidad_magica = relationship("AfinidadMagica", back_populates="solicitudes")
    status = relationship("Status", back_populates="solicitudes")
    assignments = relationship("Asignacion", back_populates="solicitud")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "identificacion": self.identificacion,
            "edad": self.edad,
            "afinidad_magica_id": self.afinidad_magica_id,
            "status_id": self.status_id
        }

class AfinidadMagica(Base):
    __tablename__ = "afinidades_magicas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), unique=True, nullable=False)
    
    solicitudes = relationship("Solicitud", back_populates="afinidad_magica")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

class Grimorio(Base):
    __tablename__ = "grimorios"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), unique=True, index=True)
    rareza = Column(String(20))
    peso = Column(Integer)

    assignments = relationship("Asignacion", back_populates="grimorio")

    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "rareza": self.rareza,
            "peso": self.peso
        }

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey('solicitudes.id'))
    grimorio_id = Column(Integer, ForeignKey('grimorios.id'))

    solicitud = relationship("Solicitud", back_populates="assignments")
    grimorio = relationship("Grimorio", back_populates="assignments")

    def serialize(self):
        return {
            "id": self.id,
            "solicitud_id": self.solicitud_id,
            "grimorio_id": self.grimorio_id,
            "grimorio": self.grimorio.serialize()
        }
