# app/services/analysis_service.py
import asyncio
import io
import json
from typing import Optional

from fastapi import UploadFile, HTTPException, status
from pydantic import ValidationError

# Importaciones de bibliotecas externas
import google.generativeai as genai
# Ya no importamos PdfReader de pypdf

# Importaciones locales
from app.core.config import settings # Importa la configuración (API Key, Prompt)
from app.schemas.analysis import AnalysisResponse # Importa el esquema de respuesta

# --- Funciones Auxiliares ---

# Ya no necesitamos _extract_text_from_pdf

async def _call_gemini_api(pdf_content: bytes, system_prompt: str, api_key: str) -> dict:
    """
    Llama a la API de Google Gemini (modelo gemini-1.5-flash-latest)
    para analizar el contenido de un archivo PDF directamente.

    Args:
        pdf_content (bytes): El contenido binario del archivo PDF.
        system_prompt (str): Las instrucciones para el modelo Gemini.
        api_key (str): La API Key de Google AI.

    Returns:
        dict: El diccionario JSON parseado de la respuesta de Gemini.

    Raises:
        HTTPException: Si la API Key no está configurada, la llamada falla,
                       o la respuesta no es un JSON válido.
    """
    if not api_key or api_key == "NO_API_KEY_SET":
        print("Error Crítico: GEMINI_API_KEY no está configurada.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="La API Key para el servicio de IA no está configurada en el servidor."
        )
    if not system_prompt or system_prompt == "DEFAULT_PROMPT_IF_FILE_NOT_FOUND":
         print("Error Crítico: El prompt del sistema no se pudo cargar.")
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El prompt del sistema para el servicio de IA no está configurado o no se pudo leer."
        )

    try:
        # Configura la API de Google AI
        genai.configure(api_key=api_key)

        # Elige el modelo multimodal (gemini-1.5-flash es una buena opción)
        # Asegúrate de que este modelo esté disponible para tu API Key y región.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        print(f"Llamando a Gemini API (modelo: {model.model_name}) con el archivo PDF...")

        # Prepara los datos para el modelo multimodal
        # Necesitamos pasar el prompt y el archivo PDF como partes separadas.
        pdf_file_data = {
            'mime_type': 'application/pdf', # Especifica el tipo MIME del archivo
            'data': pdf_content           # El contenido binario del PDF
        }

        # El contenido que se envía es una lista: [prompt_texto, archivo_pdf]
        contents = [system_prompt, pdf_file_data]

        # Realiza la llamada a la API
        # Ajusta los parámetros de generación si es necesario (temperature, top_p, etc.)
        # generation_config = genai.types.GenerationConfig(
        #     # Asegúrate de que la respuesta sea JSON
        #     response_mime_type="application/json",
        #     # Otros parámetros si son necesarios
        #     # temperature=0.1
        # )
        # Nota: Forzar response_mime_type="application/json" puede ser útil,
        # pero también podemos confiar en que el prompt pida JSON explícitamente.
        # Lo dejaremos comentado por ahora y confiaremos en el prompt.
        response = model.generate_content(contents) # , generation_config=generation_config)

        print("Respuesta recibida de Gemini.")

        # Extrae el texto de la respuesta
        # Aunque pidamos JSON, la respuesta viene dentro de response.text
        response_text = response.text.strip()

        # Intenta parsear la respuesta como JSON
        # Limpia posibles bloques de código markdown alrededor del JSON
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
             response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        print(f"Texto JSON (limpio) de Gemini:\n{response_text}")

        analysis_result_dict = json.loads(response_text)
        return analysis_result_dict

    except json.JSONDecodeError as json_err:
        print(f"Error: La respuesta de Gemini no es un JSON válido. Error: {json_err}")
        print(f"Respuesta recibida:\n{response.text}") # Imprime la respuesta completa para depurar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El servicio de IA devolvió una respuesta en un formato inesperado (no es JSON válido)."
        )
    except Exception as e:
        # Captura otros posibles errores de la API de Gemini
        print(f"Error durante la llamada a la API de Gemini: {e}")
        # Intenta obtener más detalles si es una excepción específica de Google AI
        error_detail = str(e)
        if hasattr(e, 'message'):
             error_detail = e.message
        # Errores comunes pueden ser por permisos, cuotas, modelo no disponible, etc.
        # Un error específico podría ser google.api_core.exceptions.PermissionDenied: 403 Your API key is invalid
        print(f"Detalle del error de API: {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, # Indica un problema con el servicio externo
            detail=f"Error al comunicarse con el servicio de IA: {error_detail}"
        )

# --- Servicio Principal ---

async def analyze_pdf_document(pdf_file: UploadFile) -> AnalysisResponse:
    """
    Servicio principal para analizar un documento PDF usando Gemini Multimodal.

    Lee el archivo, lo envía directamente a la API de Gemini y valida la respuesta.

    Args:
        pdf_file (UploadFile): El objeto del archivo PDF subido.

    Returns:
        AnalysisResponse: Un objeto Pydantic con los datos del análisis validados.

    Raises:
        HTTPException: Si ocurre algún error durante el proceso.
    """
    try:
        # 1. Leer contenido del archivo PDF (como bytes)
        pdf_content = await pdf_file.read()
        if not pdf_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo PDF está vacío o no se pudo leer."
            )
        print(f"Archivo PDF leído. Tamaño: {len(pdf_content)} bytes.")
    except Exception as e:
        print(f"Error al leer el archivo UploadFile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo leer el archivo PDF subido: {e}"
        )
    finally:
        await pdf_file.close() # Cierra el archivo

    # 2. Obtener configuración (API Key y Prompt)
    api_key = settings.GEMINI_API_KEY
    system_prompt = settings.GEMINI_SYSTEM_PROMPT # Cargado desde prompt.txt

    # 3. Llamar a la API de Gemini Multimodal (maneja excepciones internamente)
    # Pasamos los bytes del PDF directamente
    analysis_result_dict = await _call_gemini_api(pdf_content, system_prompt, api_key)

    # 4. Validar la respuesta JSON con el esquema Pydantic
    try:
        # Crea una instancia del modelo Pydantic desde el diccionario devuelto por Gemini.
        analysis_response = AnalysisResponse(**analysis_result_dict)
        print("Respuesta de Gemini validada correctamente con el esquema Pydantic.")
        return analysis_response
    except ValidationError as val_err:
        # Si la validación falla
        print(f"Error: La respuesta de Gemini no cumple con el esquema AnalysisResponse. Errores: {val_err.errors()}")
        print(f"Diccionario recibido de Gemini: {analysis_result_dict}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"La respuesta del servicio de IA no tiene la estructura esperada: {val_err.errors()}"
        )
    except Exception as e:
        # Captura cualquier otro error inesperado durante la validación
        print(f"Error inesperado al validar/crear AnalysisResponse: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la respuesta del análisis."
        )

