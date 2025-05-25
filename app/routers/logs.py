# app/routers/logs.py
from fastapi import APIRouter, Depends, HTTPException, status, Request # Importa Request para obtener la IP
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.access_log import AccessLog, AccessLogCreate
from app.crud import crud_access_log # Importa el nuevo módulo CRUD

router = APIRouter(
    prefix="/logs",
    tags=["Access Logs"],
    responses={404: {"description": "No encontrado"}},
)

@router.post(
    "/access",
    response_model=AccessLog,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un evento de acceso o acción",
    description="Crea un nuevo registro en el log de acceso. La IP y el timestamp se registran automáticamente."
)
def record_access_event(
    *,
    request: Request, # Para obtener la IP del cliente
    db: Session = Depends(get_db),
    log_in: AccessLogCreate # Datos del log desde el cuerpo de la solicitud
) -> AccessLog:
    """
    Registra un evento de acceso.
    La dirección IP del cliente se obtiene del objeto Request.
    """
    client_ip = request.client.host if request.client else None
    created_log_entry = crud_access_log.create_access_log_entry(
        db=db,
        log_entry_in=log_in,
        ip_address=client_ip
    )
    return created_log_entry

@router.get(
    "/access",
    response_model=List[AccessLog],
    summary="Obtener registros de acceso",
    description="Obtiene una lista paginada de los logs de acceso, con filtros opcionales."
)
def read_access_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_identifier: Optional[str] = None,
    action_description: Optional[str] = None
) -> List[AccessLog]:
    """
    Obtiene logs de acceso con paginación y filtros.
    """
    logs = crud_access_log.get_access_logs(
        db,
        skip=skip,
        limit=limit,
        user_identifier=user_identifier,
        action_description=action_description
    )
    return logs