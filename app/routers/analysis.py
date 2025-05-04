# app/routers/analysis.py
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from typing import Annotated # Usar Annotated para Depends y otros metadatos

from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import analyze_pdf_document

# Crea una instancia de APIRouter. Todas las rutas definidas aquí
# tendrán el prefijo que se configure en main.py (ej. /api/v1)
router = APIRouter(
    tags=["Analysis"], # Etiqueta para agrupar en la documentación de Swagger/OpenAPI
    responses={404: {"description": "No encontrado"}}, # Respuesta común para este router
)

@router.post(
    "/analyze-pdf",
    response_model=AnalysisResponse, # Especifica el modelo Pydantic para la respuesta
    summary="Analiza un oficio judicial en formato PDF",
    description="Recibe un archivo PDF, lo envía (simuladamente) a un servicio de IA para análisis "
                "y devuelve la información estructurada extraída.",
    status_code=status.HTTP_200_OK # Código de estado para respuesta exitosa
)
async def analyze_pdf_endpoint(
    # Define el parámetro 'file' que espera un archivo subido.
    # File(...) indica que es un campo obligatorio.
    file: UploadFile = File(..., description="Archivo PDF (oficio judicial) a analizar.")
):
    """
    Endpoint para recibir y procesar un archivo PDF.

    - Valida que el archivo sea de tipo 'application/pdf'.
    - Delega el procesamiento al servicio `analyze_pdf_document`.
    - Devuelve la respuesta estructurada o un error HTTP.
    """
    # 1. Validación del tipo de archivo
    if file.content_type != "application/pdf":
        print(f"Error: Tipo de archivo no válido: {file.content_type}. Se esperaba application/pdf.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no válido: '{file.content_type}'. Solo se aceptan archivos PDF (application/pdf)."
        )

    print(f"Archivo recibido: {file.filename}, Tipo: {file.content_type}")

    # 2. Llamada al servicio para procesar el archivo
    # El servicio se encargará de la lógica principal, incluyendo la simulación de Gemini.
    # El manejo de excepciones dentro del servicio devolverá HTTPException si algo falla.
    try:
        analysis_result = await analyze_pdf_document(pdf_file=file)
        # Si el servicio se completa correctamente, devuelve el resultado.
        # FastAPI se encargará de serializar el objeto AnalysisResponse a JSON.
        return analysis_result
    except HTTPException as http_exc:
        # Si el servicio lanzó una HTTPException, la relanzamos para que FastAPI la maneje.
        raise http_exc
    except Exception as e:
        # Captura cualquier otra excepción inesperada que no sea HTTPException
        print(f"Error inesperado en el endpoint /analyze-pdf: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error interno inesperado en el servidor: {e}"
        )

# Aquí podrían añadirse más endpoints relacionados con el análisis si fuera necesario.
