# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine.url import make_url # Importar make_url

from alembic import context

# --- Añadir el directorio de la app al sys.path ---
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, APP_DIR)
# --- Fin Añadir sys.path ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Configuración del Target Metadata ---
from app.db.base_class import Base
from app.models.expediente import Expediente
from app.models.access_log import AccessLog 
# from app.models.user import User # Importar otros modelos si existen

target_metadata = Base.metadata
# --- Fin Configuración Metadata ---


def get_database_url():
    """Obtiene la URL de la base de datos desde nuestra configuración centralizada."""
    from app.core.config import settings
    db_url_str = str(settings.DATABASE_URL)

    # --- CORRECCIÓN PARA HEROKU ---
    # Si la URL de Heroku viene como "postgres://...", cambiarla a "postgresql+psycopg2://..."
    if db_url_str.startswith("postgres://"):
        db_url_str = db_url_str.replace("postgres://", "postgresql+psycopg2://", 1)
        print(f"DEBUG (Alembic): URL de Heroku modificada a: {db_url_str}") # Log para verificar
    # --- FIN CORRECCIÓN ---

    return db_url_str


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url() # Obtenemos la URL (ya corregida si es necesario)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        naming_convention=target_metadata.naming_convention,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Obtenemos la URL de la base de datos (ya corregida si es necesario)
    db_url = get_database_url()

    # Creamos la configuración para el engine a partir de la URL
    # No necesitamos modificar la config aquí si db_url ya está corregida
    connectable_config = config.get_section(config.config_ini_section, {})
    connectable_config["sqlalchemy.url"] = db_url # Usamos la URL potencialmente corregida

    connectable = engine_from_config(
        connectable_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            naming_convention=target_metadata.naming_convention,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
