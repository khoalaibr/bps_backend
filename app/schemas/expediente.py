# app/schemas/expediente.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime # Para los campos de fecha

# --- Esquema Base ---
# Contiene los campos comunes que se comparten entre creación y lectura.
class ExpedienteBase(BaseModel):
    expediente_nro: str = Field(..., example="IUE 500-123/2025", description="Número o identificador del expediente")
    usuario_id: Optional[int] = Field(None, description="ID del usuario asociado (opcional)")
    trabajado: bool = Field(default=False, description="Indica si el expediente ha sido trabajado")

# --- Esquema para Creación ---
# Hereda de ExpedienteBase. Se usa para validar los datos al crear un nuevo expediente.
# No incluye 'id', 'fecha_creacion', 'fecha_actualizacion' porque son generados por la DB.
class ExpedienteCreate(ExpedienteBase):
    # Puedes añadir validaciones específicas para la creación aquí si es necesario
    pass # No necesita campos adicionales por ahora

# --- Esquema para Actualización ---
# Hereda de ExpedienteBase, pero todos los campos son opcionales.
# Permite actualizaciones parciales (ej. solo cambiar 'trabajado').
class ExpedienteUpdate(BaseModel):
    expediente_nro: Optional[str] = Field(None, example="IUE 500-123/2025", description="Número o identificador del expediente")
    usuario_id: Optional[int] = Field(None, description="ID del usuario asociado (opcional)")
    trabajado: Optional[bool] = Field(None, description="Indica si el expediente ha sido trabajado")

# --- Esquema Base para Lectura (desde DB) ---
# Hereda de ExpedienteBase y añade los campos que existen en el modelo SQLAlchemy
# pero que no se proporcionan al crear/actualizar (id, fechas).
class ExpedienteInDBBase(ExpedienteBase):
    id: int = Field(..., description="ID único del expediente")
    fecha_creacion: datetime = Field(..., description="Fecha de creación del registro")
    # fecha_actualizacion puede ser None si nunca se ha actualizado
    fecha_actualizacion: Optional[datetime] = Field(None, description="Fecha de última actualización")

    # Configuración para permitir mapeo desde el modelo SQLAlchemy
    class Config:
        from_attributes = True # Permite crear el esquema desde el objeto ORM

# --- Esquema para Devolver en la API ---
# Este es el esquema que se usará como response_model en las rutas API.
# Hereda todos los campos de ExpedienteInDBBase.
class Expediente(ExpedienteInDBBase):
    # Puedes añadir campos calculados o formateados aquí si es necesario en el futuro
    pass # No necesita campos adicionales por ahora

# --- Esquema para Lista de Expedientes (Opcional pero útil) ---
# Para devolver múltiples expedientes de forma estructurada.
class ExpedienteList(BaseModel):
    expedientes: List[Expediente]
    total: int = Field(..., example=42, description="Número total de expedientes encontrados")

