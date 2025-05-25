# app/models/access_log.py
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB # Para el campo 'details' si quieres usar JSON nativo de PG
from app.db.base_class import Base

class AccessLog(Base):
    """
    Modelo SQLAlchemy para la tabla 'access_logs'.
    Registra eventos de acceso o acciones en la aplicación.
    """
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único del registro de acceso")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True, comment="Fecha y hora del evento")
    ip_address = Column(String(45), nullable=True, comment="Dirección IP del cliente que generó el evento") # IPv4 e IPv6
    action_description = Column(String, nullable=False, index=True, comment="Descripción de la acción o evento registrado")
    # user_identifier puede ser un email, ID de usuario, o un identificador de sesión.
    # Lo dejamos como String para flexibilidad.
    user_identifier = Column(String, nullable=True, index=True, comment="Identificador del usuario (si está disponible)")
    # El campo 'details' puede almacenar información adicional en formato JSON o texto.
    # Usar JSONB es más eficiente en PostgreSQL si vas a consultarlo.
    # Si prefieres texto simple, usa Text.
    details = Column(JSONB, nullable=True, comment="Detalles adicionales sobre el evento en formato JSON")
    # Alternativa para details si no quieres usar JSONB:
    # details = Column(Text, nullable=True, comment="Detalles adicionales sobre el evento")

    def __repr__(self):
        return f"<AccessLog(id={self.id}, action='{self.action_description}', ip='{self.ip_address}')>"