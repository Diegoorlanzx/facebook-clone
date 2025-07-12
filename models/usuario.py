from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.conexion import Base  # <-- Ajuste importante aquí

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
