# app/schemas/expediente.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date # Importa date

# --- Esquema Base ---
class ExpedienteBase(BaseModel):
    expediente_nro: str = Field(..., example="IUE 500-123/2025", description="Número o identificador del expediente")
    usuario_id: Optional[int] = Field(None, description="ID del usuario asociado (opcional)")
    trabajado: bool = Field(default=False, description="Indica si el expediente ha sido trabajado")
    # --- Nuevos campos base ---
    oficio: Optional[str] = Field(None, example="250/2025", description="Número de oficio")
    fecha_recibido: Optional[date] = Field(None, example="2025-05-07", description="Fecha en que se recibió el oficio (YYYY-MM-DD)")
    juzgado: Optional[str] = Field(None, example="Juzgado Letrado de Rivera de 4° Turno", description="Nombre del Juzgado emisor")
    departamento: Optional[str] = Field(None, example="Rivera", description="Departamento del Juzgado emisor")

# --- Esquema para Creación ---
class ExpedienteCreate(ExpedienteBase):
    # Hereda todos los campos de ExpedienteBase
    # Asegúrate de que los campos requeridos al crear estén marcados como no opcionales
    # en ExpedienteBase si es necesario (ej. expediente_nro = Field(...))
    pass

# --- Esquema para Actualización ---
# Todos los campos son opcionales para permitir actualizaciones parciales
class ExpedienteUpdate(BaseModel):
    expediente_nro: Optional[str] = Field(None, example="IUE 500-123/2025")
    usuario_id: Optional[int] = Field(None)
    trabajado: Optional[bool] = Field(None)
    oficio: Optional[str] = Field(None, example="250/2025")
    fecha_recibido: Optional[date] = Field(None, example="2025-05-07")
    juzgado: Optional[str] = Field(None, example="Juzgado Letrado de Rivera de 4° Turno")
    departamento: Optional[str] = Field(None, example="Rivera")

# --- Esquema Base para Lectura (desde DB) ---
class ExpedienteInDBBase(ExpedienteBase):
    id: int = Field(..., description="ID único del expediente")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del registro")
    fecha_actualizacion: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        from_attributes = True # Permite mapeo desde el modelo SQLAlchemy

# --- Esquema para Devolver en la API ---
class Expediente(ExpedienteInDBBase):
    # Hereda todos los campos, incluyendo los nuevos de ExpedienteBase
    pass

# --- Esquema para Lista de Expedientes ---
class ExpedienteList(BaseModel):
    expedientes: List[Expediente]
    total: int = Field(..., example=42)

