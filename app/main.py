# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa los routers
from app.routers import analysis, expedientes # Añade el nuevo router de expedientes
from app.core.config import settings

# Crea la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="API de Análisis y Gestión de Oficios",
    description="API para analizar oficios judiciales PDF y gestionar expedientes asociados.",
    version="0.2.0", # Incrementamos versión
)

# --- Configuración de CORS ---
origins = ["*"] # ¡Recuerda cambiar esto en producción!

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin de Configuración de CORS ---


# --- Incluir Routers ---
# Incluye el router de análisis (existente)
app.include_router(analysis.router, prefix="/api/v1")
# Incluye el nuevo router de expedientes
app.include_router(expedientes.router, prefix="/api/v1") # Usamos el mismo prefijo base

# --- Endpoint Raíz ---
@app.get("/", tags=["Root"], summary="Verifica si la API está activa")
async def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de Análisis y Gestión de Oficios"}

# Nota: Aún no hemos creado las tablas en la base de datos.
# El siguiente paso será usar Alembic para eso.

