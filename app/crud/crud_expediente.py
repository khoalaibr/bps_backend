# app/crud/crud_expediente.py
from sqlalchemy.orm import Session
from typing import List, Optional, Type

from app.models.expediente import Expediente # Importa el modelo SQLAlchemy
from app.schemas.expediente import ExpedienteCreate, ExpedienteUpdate # Importa los esquemas Pydantic

# --- Operaciones CRUD para Expediente ---

def get_expediente(db: Session, expediente_id: int) -> Optional[Expediente]:
    """
    Obtiene un expediente específico por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        expediente_id (int): El ID del expediente a buscar.

    Returns:
        Optional[Expediente]: El objeto Expediente si se encuentra, None si no.
    """
    return db.query(Expediente).filter(Expediente.id == expediente_id).first()

def get_expedientes(db: Session, skip: int = 0, limit: int = 100) -> List[Type[Expediente]]:
    """
    Obtiene una lista de expedientes, con opción de paginación.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a saltar (para paginación).
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[Type[Expediente]]: Una lista de objetos Expediente.
    """
    return db.query(Expediente).offset(skip).limit(limit).all()

def get_expediente_by_nro(db: Session, expediente_nro: str) -> Optional[Expediente]:
    """
    Obtiene un expediente específico por su número de expediente.
    (Útil para evitar duplicados si el número debe ser único).

    Args:
        db (Session): La sesión de la base de datos.
        expediente_nro (str): El número de expediente a buscar.

    Returns:
        Optional[Expediente]: El objeto Expediente si se encuentra, None si no.
    """
    return db.query(Expediente).filter(Expediente.expediente_nro == expediente_nro).first()


def create_expediente(db: Session, expediente: ExpedienteCreate) -> Expediente:
    """
    Crea un nuevo registro de expediente en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        expediente (ExpedienteCreate): Los datos del expediente a crear (validados por Pydantic).

    Returns:
        Expediente: El objeto Expediente recién creado.
    """
    # Crea una instancia del modelo SQLAlchemy a partir de los datos del esquema Pydantic
    db_expediente = Expediente(
        expediente_nro=expediente.expediente_nro,
        usuario_id=expediente.usuario_id,
        trabajado=expediente.trabajado
        # Nota: id, fecha_creacion, fecha_actualizacion son manejados por la DB/SQLAlchemy
    )
    db.add(db_expediente) # Añade el nuevo objeto a la sesión
    db.commit() # Confirma la transacción para guardar en la DB
    db.refresh(db_expediente) # Refresca el objeto para obtener los valores generados por la DB (como el id)
    return db_expediente

def update_expediente(
    db: Session,
    db_obj: Expediente,
    obj_in: ExpedienteUpdate
) -> Expediente:
    """
    Actualiza un expediente existente en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        db_obj (Expediente): El objeto Expediente existente (obtenido previamente).
        obj_in (ExpedienteUpdate): Los datos a actualizar (validados por Pydantic).

    Returns:
        Expediente: El objeto Expediente actualizado.
    """
    # Convierte el esquema Pydantic a un diccionario, excluyendo valores no establecidos
    update_data = obj_in.model_dump(exclude_unset=True)

    # Actualiza los campos del objeto SQLAlchemy existente
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj) # Añade el objeto modificado a la sesión
    db.commit() # Confirma la transacción
    db.refresh(db_obj) # Refresca el objeto
    return db_obj

def update_trabajado_status(db: Session, expediente_id: int, trabajado: bool) -> Optional[Expediente]:
    """
    Actualiza únicamente el estado 'trabajado' de un expediente.

    Args:
        db (Session): La sesión de la base de datos.
        expediente_id (int): El ID del expediente a actualizar.
        trabajado (bool): El nuevo estado (True o False).

    Returns:
        Optional[Expediente]: El objeto Expediente actualizado si se encontró, None si no.
    """
    db_expediente = get_expediente(db, expediente_id=expediente_id)
    if not db_expediente:
        return None # O podrías lanzar una excepción

    db_expediente.trabajado = trabajado
    db.add(db_expediente)
    db.commit()
    db.refresh(db_expediente)
    return db_expediente


def delete_expediente(db: Session, expediente_id: int) -> Optional[Expediente]:
    """
    Elimina un expediente de la base de datos por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        expediente_id (int): El ID del expediente a eliminar.

    Returns:
        Optional[Expediente]: El objeto Expediente eliminado si se encontró, None si no.
    """
    db_expediente = get_expediente(db, expediente_id=expediente_id)
    if not db_expediente:
        return None # O podrías lanzar una excepción

    db.delete(db_expediente) # Marca el objeto para eliminación
    db.commit() # Confirma la transacción
    # Nota: No se puede hacer refresh a un objeto eliminado
    return db_expediente # Devuelve el objeto tal como estaba antes de eliminar (opcional)

