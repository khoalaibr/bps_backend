# app/db/base_class.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Opcional: Define convenciones de nomenclatura para índices y claves foráneas
# Esto ayuda a tener nombres consistentes generados por Alembic.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Crea una instancia de MetaData con las convenciones de nomenclatura
metadata = MetaData(naming_convention=convention)

# Define la clase base declarativa usando la metadata configurada
class Base(DeclarativeBase):
    metadata = metadata
