# app/schemas/analysis.py
from pydantic import BaseModel, Field, field_validator # Import field_validator if needed
from typing import List, Optional, Union # Import Union if needed for mixed types

# --- Esquemas Anidados para Acciones Detalladas ---

class InvolucradoAccion(BaseModel):
    """Esquema para una persona involucrada en una acción específica."""
    rol: Optional[str] = Field(None, description="Rol de la persona en la acción (ej: Solicitante, Beneficiario)")
    nombre_completo: Optional[str] = Field(None, description="Nombre completo de la persona")
    documento_identidad: Optional[str] = Field(None, description="C.I. de la persona (solo números)")

    # Opcional: Añadir un validador para asegurar que documento_identidad solo contenga números
    @field_validator('documento_identidad')
    def validate_doc_identidad(cls, v):
        if v is not None and not v.isdigit():
            # Podrías intentar limpiarlo o lanzar un error, por ahora lo dejamos pasar
            # raise ValueError('Documento de identidad debe contener solo números')
            print(f"Advertencia: documento_identidad '{v}' contiene caracteres no numéricos.")
        return v

class AccionDetallada(BaseModel):
    """Esquema para una acción detallada extraída del oficio."""
    tipo_accion: str = Field(..., description="Clasificación de la acción (ej: Solicitud de Historia Laboral)")
    descripcion_completa: str = Field(..., description="Descripción explícita de la acción, mencionando involucrados")
    involucrados_accion: List[InvolucradoAccion] = Field([], description="Lista de personas involucradas específicamente en esta acción")

# --- Esquema Principal de Respuesta del Análisis ---

class AnalysisResponse(BaseModel):
    """
    Esquema Pydantic para la respuesta del análisis del PDF,
    alineado con la nueva estructura del prompt.
    """
    # Datos del Juzgado
    codigo_juzgado: Optional[int] = Field(None, example=163553, description="Código numérico del Juzgado según tabla de mapeo, o null si no se encuentra.")
    nombre_juzgado: Optional[str] = Field(None, example="Juzgado Letrado de Rivera de 4° Turno", description="Nombre completo del Juzgado emisor.")
    email_juzgado: Optional[str] = Field(None, example="jrivera4@poderjudicial.gub.uy", description="Email del Juzgado emisor.")
    departamento_juzgado: Optional[str] = Field(None, example="Rivera", description="Departamento del Juzgado emisor.")

    # Datos del Oficio/Caso
    documentos_involucrados: List[str] = Field([], example=["44594247"], description="Lista de C.I. numéricas de las partes principales mencionadas en el oficio.")
    asunto_principal: str = Field(..., example="Oficio N° 250/2025 – Juzgado ... - Autos: \"...\", IUE ... – Solicitud...", description="Resumen del asunto general del oficio.")
    cve: Optional[str] = Field(None, example="A1B2C3D4E5", description="Código de Verificación Electrónica (CVE) si se encuentra.")

    # Acciones Específicas
    acciones_detalladas: List[AccionDetallada] = Field([], description="Lista detallada de acciones solicitadas o comunicadas.")

    # Secreto Tributario
    releva_secreto_tributario: bool = Field(..., description="Indica si el oficio releva el secreto tributario.")
    justificacion_releva_secreto: Optional[str] = Field(None, description="Frase exacta del oficio que justifica la relevación del secreto, si aplica.")

    # Opcional: Validadores adicionales si son necesarios
    @field_validator('documentos_involucrados', mode='before')
    def validate_docs_involucrados(cls, v):
        if not isinstance(v, list):
            return [] # Devuelve lista vacía si no es una lista
        # Asegura que todos los elementos sean strings y numéricos
        validated_docs = []
        for item in v:
            if isinstance(item, (str, int)):
                doc_str = str(item).strip()
                if doc_str.isdigit():
                    validated_docs.append(doc_str)
                else:
                     print(f"Advertencia: documento_involucrado '{doc_str}' no es numérico.")
                     # Podrías decidir incluirlo igualmente o filtrarlo
                     # validated_docs.append(doc_str) # Descomentar si quieres incluir no numéricos
            else:
                print(f"Advertencia: elemento no válido en documentos_involucrados: {item}")
        return validated_docs


    class Config:
        # Permite la creación desde atributos (útil si Gemini devolviera un objeto)
        from_attributes = True
