# app/crud/crud_expediente.py
from sqlalchemy.orm import Session
from typing import List, Optional, Type

from app.models.expediente import Expediente
from app.schemas.expediente import ExpedienteCreate, ExpedienteUpdate

# --- Operaciones CRUD para Expediente ---

def get_expediente(db: Session, expediente_id: int) -> Optional[Expediente]:
    """Obtiene un expediente específico por su ID."""
    return db.query(Expediente).filter(Expediente.id == expediente_id).first()

def get_expedientes(db: Session, skip: int = 0, limit: int = 100) -> List[Type[Expediente]]:
    """Obtiene una lista de expedientes, con opción de paginación."""
    return db.query(Expediente).offset(skip).limit(limit).all()

def get_expediente_by_nro(db: Session, expediente_nro: str) -> Optional[Expediente]:
    """Obtiene un expediente específico por su número de expediente."""
    return db.query(Expediente).filter(Expediente.expediente_nro == expediente_nro).first()


def create_expediente(db: Session, expediente: ExpedienteCreate) -> Expediente:
    """Crea un nuevo registro de expediente en la base de datos."""
    # Crea una instancia del modelo SQLAlchemy incluyendo los nuevos campos
    db_expediente = Expediente(
        expediente_nro=expediente.expediente_nro,
        usuario_id=expediente.usuario_id,
        trabajado=expediente.trabajado,
        # --- Añadir nuevos campos ---
        oficio=expediente.oficio,
        fecha_recibido=expediente.fecha_recibido,
        juzgado=expediente.juzgado,
        departamento=expediente.departamento
    )
    db.add(db_expediente)
    db.commit()
    db.refresh(db_expediente)
    return db_expediente

def update_expediente(
    db: Session,
    db_obj: Expediente,
    obj_in: ExpedienteUpdate # ExpedienteUpdate ya incluye los nuevos campos opcionales
) -> Expediente:
    """Actualiza un expediente existente en la base de datos."""
    # Convierte el esquema Pydantic a un diccionario, excluyendo valores no establecidos
    update_data = obj_in.model_dump(exclude_unset=True)

    # Actualiza los campos del objeto SQLAlchemy existente
    # Esto funcionará para los campos nuevos y viejos
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_trabajado_status(db: Session, expediente_id: int, trabajado: bool) -> Optional[Expediente]:
    """Actualiza únicamente el estado 'trabajado' de un expediente."""
    db_expediente = get_expediente(db, expediente_id=expediente_id)
    if not db_expediente:
        return None

    db_expediente.trabajado = trabajado
    db.add(db_expediente)
    db.commit()
    db.refresh(db_expediente)
    return db_expediente


def delete_expediente(db: Session, expediente_id: int) -> Optional[Expediente]:
    """Elimina un expediente de la base de datos por su ID."""
    db_expediente = get_expediente(db, expediente_id=expediente_id)
    if not db_expediente:
        return None

    db.delete(db_expediente)
    db.commit()
    return db_expediente

