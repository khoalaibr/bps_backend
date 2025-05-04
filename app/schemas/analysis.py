# app/schemas/analysis.py
from pydantic import BaseModel, Field
from typing import List, Optional # Asegúrate de que Optional esté importado

class AnalysisResponse(BaseModel):
    """
    Esquema Pydantic para la respuesta del análisis del PDF.
    Define la estructura esperada del JSON devuelto por la API de Gemini.
    """
    # CORRECCIÓN: Aseguramos que el tipo sea Optional[int] para aceptar entero o null.
    codigo: Optional[int] = Field(None, example=163553, description="Código numérico del Juzgado según tabla de mapeo, o null si no se encuentra.")
    documentos: List[str] = Field(..., example=["44594247"], description="Lista de C.I. numéricas extraídas.")
    asunto: str = Field(..., example="Oficio N° 250/2025 – Juzgado Letrado de Rivera de 4° Turno - Autos: \"...\", IUE ... – Solicitud...", description="Resumen del asunto del oficio.")
    acciones: List[str] = Field(..., example=["Remitir historia laboral completa"], description="Lista de acciones específicas solicitadas.")

    class Config:
        # Permite la creación desde atributos (útil si Gemini devolviera un objeto)
        from_attributes = True # Mantenemos esto por si acaso
