# app/models/expediente.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func, ForeignKey # Importa Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Expediente(Base):
    """
    Modelo SQLAlchemy para la tabla 'expedientes'.
    """
    __tablename__ = "expedientes"

    # Columnas existentes
    id = Column(Integer, primary_key=True, index=True, comment="Identificador único del expediente")
    expediente_nro = Column(String, index=True, nullable=False, comment="Número o identificador del expediente (ej. IUE)")
    # Cuando tengas el modelo User, añadirás: ForeignKey("users.id")
    usuario_id = Column(Integer, nullable=True, index=True, comment="ID del usuario asociado (opcional por ahora)")
    # usuario_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True, comment="ID del usuario asociado (opcional por ahora)") # Añadido ForeignKey y ondelete
    trabajado = Column(Boolean, default=False, nullable=False, comment="Indica si el expediente ha sido trabajado (True) o no (False)")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="Fecha y hora de creación del registro (automática)")
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now(), comment="Fecha y hora de la última actualización (automática en updates)")

    # --- Nuevas Columnas ---
    oficio = Column(String, nullable=True, comment="Número de oficio (ej. 250/2025)")
    fecha_recibido = Column(Date, nullable=True, comment="Fecha en que se recibió el oficio")
    juzgado = Column(String, nullable=True, comment="Nombre del Juzgado emisor")
    departamento = Column(String, nullable=True, comment="Departamento del Juzgado emisor")
    # --- Fin Nuevas Columnas ---


    # --- Relaciones (Ejemplo futuro con User) ---
    # owner = relationship("User", back_populates="expedientes") # Descomentar cuando exista User
    # Asegúrate de añadir la relación inversa "expedientes = relationship('Expediente', back_populates='owner')" en el modelo User.

    def __repr__(self):
        return f"<Expediente(id={self.id}, nro='{self.expediente_nro}', oficio='{self.oficio}')>"

# --- Modelo User (Ejemplo Básico - Crear en app/models/user.py si no existe) ---
# Necesitamos definir al menos un modelo User básico para que la ForeignKey funcione
# Si ya tienes un modelo User, asegúrate de que tenga la relación inversa.
# Si no, crea app/models/user.py con algo como esto:

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     # ... otros campos de usuario ...
#
#     # Relación inversa con Expediente
#     expedientes = relationship("Expediente", back_populates="owner") # 'owner' debe coincidir con el nombre en Expediente

# ¡Importante! Asegúrate de importar el modelo User en alembic/env.py también
# from app.models.user import User
