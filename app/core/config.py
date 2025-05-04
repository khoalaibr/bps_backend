# app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn # Validador específico para URLs de PostgreSQL

# --- Cargar variables desde .env ---
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
print(f"DEBUG: Intentando cargar .env desde: {env_path}")
if os.path.exists(env_path):
    loaded = load_dotenv(dotenv_path=env_path, verbose=True, override=True)
    print(f"DEBUG: load_dotenv ejecutado. ¿Cargó variables? {loaded}")
else:
    print(f"DEBUG: Archivo .env NO encontrado en {env_path}")
# --- Fin carga .env ---

# --- Cargar el Prompt desde prompt.txt ---
prompt_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'prompt.txt')
print(f"DEBUG: Intentando cargar prompt desde: {prompt_file_path}")
SYSTEM_PROMPT_FROM_FILE = "DEFAULT_PROMPT_IF_FILE_NOT_FOUND"
try:
    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            SYSTEM_PROMPT_FROM_FILE = f.read()
        print(f"DEBUG: Prompt cargado desde {prompt_file_path}. Longitud: {len(SYSTEM_PROMPT_FROM_FILE)}")
    else:
        print(f"DEBUG: Archivo prompt.txt NO encontrado en {prompt_file_path}")
except Exception as e:
    print(f"ERROR: No se pudo leer el archivo prompt.txt: {e}")
# --- Fin carga prompt.txt ---


class Settings(BaseSettings):
    """
    Configuraciones de la aplicación.
    """
    # Lee la API Key desde el entorno
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "NO_API_KEY_SET")

    # El prompt ahora se asigna directamente desde la variable leída del archivo
    GEMINI_SYSTEM_PROMPT: str = SYSTEM_PROMPT_FROM_FILE

    # --- Nueva Configuración de Base de Datos ---
    # Lee la URL de la base de datos desde el entorno
    # Usamos PostgresDsn para validar que el formato sea correcto
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@host:port/db")

    class Config:
        env_file_encoding = 'utf-8'
        extra = "ignore"

# Instancia global de configuraciones.
settings = Settings()

# --- Línea de Depuración ---
print("-" * 50)
print(f"DEBUG (Settings): GEMINI_API_KEY cargada: {settings.GEMINI_API_KEY[:4]}...{settings.GEMINI_API_KEY[-4:] if len(settings.GEMINI_API_KEY) > 8 else settings.GEMINI_API_KEY}")
# print(f"DEBUG (Settings): GEMINI_SYSTEM_PROMPT cargado: '{settings.GEMINI_SYSTEM_PROMPT[:50]}...'") # Opcional mostrar prompt
print(f"DEBUG (Settings): DATABASE_URL cargada: {str(settings.DATABASE_URL)}") # Muestra la URL parseada
print("-" * 50)
# --- Fin Línea de Depuración ---
