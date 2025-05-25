# app/crud/crud_access_log.py
from sqlalchemy.orm import Session
from typing import List, Optional, Type, Dict, Any

from app.models.access_log import AccessLog # Modelo SQLAlchemy
from app.schemas.access_log import AccessLogCreate # Esquema Pydantic para creación

def create_access_log_entry(
    db: Session,
    *,
    log_entry_in: AccessLogCreate, # Datos que vienen de la solicitud
    ip_address: Optional[str] = None # La IP se obtendrá de la solicitud en el router
) -> AccessLog:
    """
    Crea un nuevo registro de log de acceso en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        log_entry_in (AccessLogCreate): Datos del log a crear.
        ip_address (Optional[str]): Dirección IP del solicitante.

    Returns:
        AccessLog: El objeto AccessLog recién creado.
    """
    db_log_entry = AccessLog(
        ip_address=ip_address,
        action_description=log_entry_in.action_description,
        user_identifier=log_entry_in.user_identifier,
        details=log_entry_in.details
        # timestamp es manejado por server_default=func.now()
    )
    db.add(db_log_entry)
    db.commit()
    db.refresh(db_log_entry)
    return db_log_entry

def get_access_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_identifier: Optional[str] = None,
    action_description: Optional[str] = None
) -> List[Type[AccessLog]]:
    """
    Obtiene una lista de registros de acceso, con filtros opcionales y paginación.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a saltar.
        limit (int): Número máximo de registros a devolver.
        user_identifier (Optional[str]): Filtrar por identificador de usuario.
        action_description (Optional[str]): Filtrar por descripción de acción (búsqueda parcial).

    Returns:
        List[Type[AccessLog]]: Una lista de objetos AccessLog.
    """
    query = db.query(AccessLog)
    if user_identifier:
        query = query.filter(AccessLog.user_identifier == user_identifier)
    if action_description:
        query = query.filter(AccessLog.action_description.ilike(f"%{action_description}%")) # Búsqueda case-insensitive

    return query.order_by(AccessLog.timestamp.desc()).offset(skip).limit(limit).all()

