# app/routers/expedientes.py
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Any # Importa Any para el response de delete

from app.db.session import get_db # Dependencia para obtener la sesión DB
from app.schemas.expediente import Expediente, ExpedienteCreate, ExpedienteUpdate # Esquemas Pydantic
from app.crud import crud_expediente # Funciones CRUD

# Crea un nuevo router para los endpoints de expedientes
router = APIRouter(
    prefix="/expedientes", # Prefijo para todas las rutas en este archivo
    tags=["Expedientes"], # Etiqueta para la documentación de Swagger UI
    responses={404: {"description": "Expediente no encontrado"}}, # Respuesta común
)

# --- Endpoint para Crear un Expediente ---
@router.post(
    "/",
    response_model=Expediente, # El tipo de dato que devolverá (validado por Pydantic)
    status_code=status.HTTP_201_CREATED, # Código de estado para creación exitosa
    summary="Crear un nuevo expediente",
    description="Crea un nuevo registro de expediente en la base de datos."
)
def create_new_expediente(
    *, # Fuerza a que los siguientes argumentos sean keyword-only
    db: Session = Depends(get_db), # Inyecta la sesión de la DB
    expediente_in: ExpedienteCreate # Espera un cuerpo de solicitud que coincida con ExpedienteCreate
) -> Expediente:
    """
    Crea un nuevo expediente.
    - Verifica si ya existe un expediente con el mismo número (opcional, descomentar si es necesario).
    - Llama a la función CRUD para crear el expediente.
    """
    # Opcional: Verificar si ya existe un expediente con ese número
    # existing_expediente = crud_expediente.get_expediente_by_nro(db, expediente_nro=expediente_in.expediente_nro)
    # if existing_expediente:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Ya existe un expediente con el número '{expediente_in.expediente_nro}'."
    #     )

    # Llama a la función CRUD para crear
    created_expediente = crud_expediente.create_expediente(db=db, expediente=expediente_in)
    return created_expediente

# --- Endpoint para Obtener una Lista de Expedientes ---
@router.get(
    "/",
    response_model=List[Expediente], # Devuelve una lista de expedientes
    summary="Obtener lista de expedientes",
    description="Obtiene una lista paginada de todos los expedientes registrados."
)
def read_expedientes(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar (paginación)"),
    limit: int = Query(100, ge=1, le=200, description="Número máximo de registros a devolver (máx 200)")
) -> List[Expediente]:
    """
    Obtiene una lista de expedientes con paginación.
    """
    expedientes = crud_expediente.get_expedientes(db, skip=skip, limit=limit)
    return expedientes # FastAPI convertirá automáticamente los objetos SQLAlchemy a JSON usando el response_model

# --- Endpoint para Obtener un Expediente por ID ---
@router.get(
    "/{expediente_id}",
    response_model=Expediente,
    summary="Obtener un expediente por ID",
    description="Obtiene los detalles de un expediente específico usando su ID."
)
def read_expediente_by_id(
    expediente_id: int = Path(..., description="ID del expediente a obtener", gt=0),
    db: Session = Depends(get_db)
) -> Expediente:
    """
    Obtiene un expediente por su ID.
    - Llama a la función CRUD para buscar el expediente.
    - Si no se encuentra, lanza una excepción HTTP 404.
    """
    db_expediente = crud_expediente.get_expediente(db, expediente_id=expediente_id)
    if db_expediente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expediente con ID {expediente_id} no encontrado"
        )
    return db_expediente

# --- Endpoint para Actualizar un Expediente (Parcial - PATCH) ---
@router.patch(
    "/{expediente_id}",
    response_model=Expediente,
    summary="Actualizar un expediente (parcial)",
    description="Actualiza uno o más campos de un expediente existente. Solo se modifican los campos proporcionados."
)
def update_existing_expediente(
    expediente_id: int = Path(..., description="ID del expediente a actualizar", gt=0),
    *,
    db: Session = Depends(get_db),
    expediente_in: ExpedienteUpdate # Espera un cuerpo con los campos a actualizar
) -> Expediente:
    """
    Actualiza un expediente existente.
    - Busca el expediente por ID.
    - Si no existe, lanza 404.
    - Llama a la función CRUD para actualizar los campos proporcionados.
    """
    db_expediente = crud_expediente.get_expediente(db, expediente_id=expediente_id)
    if not db_expediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expediente con ID {expediente_id} no encontrado para actualizar"
        )
    # Llama a la función CRUD de actualización
    updated_expediente = crud_expediente.update_expediente(db=db, db_obj=db_expediente, obj_in=expediente_in)
    return updated_expediente

# --- Endpoint para Actualizar el Estado 'Trabajado' ---
@router.patch(
    "/{expediente_id}/trabajado",
    response_model=Expediente,
    summary="Actualizar estado 'trabajado'",
    description="Cambia el estado booleano 'trabajado' de un expediente específico."
)
def update_expediente_trabajado_status(
    expediente_id: int = Path(..., description="ID del expediente a modificar", gt=0),
    trabajado: bool = Body(..., description="Nuevo estado 'trabajado' (true o false)"), # Espera el booleano en el cuerpo
    db: Session = Depends(get_db)
) -> Expediente:
    """
    Actualiza el estado 'trabajado' de un expediente.
    - Llama a la función CRUD específica para esta acción.
    - Si el expediente no existe, lanza 404.
    """
    updated_expediente = crud_expediente.update_trabajado_status(db=db, expediente_id=expediente_id, trabajado=trabajado)
    if not updated_expediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expediente con ID {expediente_id} no encontrado para actualizar estado"
        )
    return updated_expediente

# --- Endpoint para Eliminar un Expediente ---
@router.delete(
    "/{expediente_id}",
    status_code=status.HTTP_204_NO_CONTENT, # Código estándar para eliminación exitosa sin contenido de respuesta
    summary="Eliminar un expediente",
    description="Elimina permanentemente un registro de expediente de la base de datos.",
    # response_model=None es implícito con 204, pero podemos devolver un mensaje si quisiéramos
    # response_model=dict # Si quisiéramos devolver {"message": "Expediente eliminado"}
)
def delete_existing_expediente(
    expediente_id: int = Path(..., description="ID del expediente a eliminar", gt=0),
    db: Session = Depends(get_db)
) -> None: # Devuelve None porque el status code es 204
    """
    Elimina un expediente por su ID.
    - Llama a la función CRUD para eliminar.
    - Si no se encuentra, lanza 404.
    """
    deleted_expediente = crud_expediente.delete_expediente(db=db, expediente_id=expediente_id)
    if not deleted_expediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expediente con ID {expediente_id} no encontrado para eliminar"
        )
    # No se devuelve nada en el cuerpo con status 204
    return None
    # Si usaras status 200, podrías devolver:
    # return {"message": f"Expediente con ID {expediente_id} eliminado exitosamente"}

