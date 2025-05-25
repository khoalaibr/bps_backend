# app/schemas/access_log.py
from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Optional, Dict, Any
from datetime import datetime

# --- Esquema para la Creación de un Registro de Acceso ---
# Esto es lo que el frontend enviará (o la app internamente construirá).
# ip_address y timestamp serán manejados por el backend.
class AccessLogCreate(BaseModel):
    action_description: str = Field(..., example="Clicked 'Analyze PDF' button", description="Descripción de la acción o evento.")
    user_identifier: Optional[str] = Field(None, example="usuario@example.com", description="Identificador del usuario (email, ID, etc.), si está disponible.")
    details: Optional[Dict[str, Any]] = Field(None, example={"filename": "oficio123.pdf", "expediente_id": 1}, description="Detalles adicionales en formato JSON.")

# --- Esquema para Devolver un Registro de Acceso en la API ---
# Esto es lo que la API devolverá al leer los logs.
class AccessLog(BaseModel):
    id: int
    timestamp: datetime
    ip_address: Optional[IPvAnyAddress] = None # Pydantic puede validar IPs
    action_description: str
    user_identifier: Optional[str] = None
    details: Optional[Dict[str, Any]] = None # O simplemente 'Any' si el JSON es muy variable

    class Config:
        from_attributes = True # Para mapear desde el objeto SQLAlchemy