# app/models/expediente.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey # Importa los tipos necesarios
from sqlalchemy.orm import relationship # Para futuras relaciones
from app.db.base_class import Base # Importa la clase Base

class Expediente(Base):
    """
    Modelo SQLAlchemy para la tabla 'expedientes'.
    """
    __tablename__ = "expedientes" # Nombre de la tabla en la base de datos

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True, comment="Identificador único del expediente")
    expediente_nro = Column(String, index=True, nullable=False, comment="Número o identificador del expediente (ej. IUE)")
    # usuario_id será opcional por ahora (nullable=True).
    # Cuando tengas el modelo User, añadirás: ForeignKey("users.id")
    usuario_id = Column(Integer, nullable=True, index=True, comment="ID del usuario asociado (opcional por ahora)")
    trabajado = Column(Boolean, default=False, nullable=False, comment="Indica si el expediente ha sido trabajado (True) o no (False)")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="Fecha y hora de creación del registro (automática)")
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now(), comment="Fecha y hora de la última actualización (automática en updates)")

    # --- Relaciones (Ejemplo futuro) ---
    # Si tuvieras un modelo User:
    # owner = relationship("User", back_populates="expedientes")
    # Asegúrate de añadir la relación inversa "expedientes" en el modelo User.

    def __repr__(self):
        return f"<Expediente(id={self.id}, nro='{self.expediente_nro}', trabajado={self.trabajado})>"
