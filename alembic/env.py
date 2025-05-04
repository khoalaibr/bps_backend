# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Añadir el directorio de la app al sys.path ---
# Esto permite que Alembic encuentre nuestros módulos (models, core, etc.)
# Ajusta la ruta si tu estructura es diferente
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, APP_DIR)
# --- Fin Añadir sys.path ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Configuración del Target Metadata ---
# Importa la clase Base de nuestro proyecto y otros modelos necesarios
from app.db.base_class import Base # Importa nuestra Base declarativa
# Asegúrate de importar todos los modelos para que Alembic los detecte
# Aunque no se usen directamente aquí, la importación los registra en Base.metadata
from app.models.expediente import Expediente
# from app.models.user import User # Ejemplo si tuvieras más modelos

# Establece el target_metadata con la metadata de nuestra Base
target_metadata = Base.metadata
# --- Fin Configuración Metadata ---

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_database_url():
    """Obtiene la URL de la base de datos desde nuestra configuración centralizada."""
    from app.core.config import settings # Importa las configuraciones de la app
    return str(settings.DATABASE_URL) # Devuelve la URL como string


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url") # Ya no leemos de alembic.ini
    url = get_database_url() # Obtenemos la URL desde nuestra config
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Añade la convención de nombres aquí también si es necesario
        # No es estrictamente necesario si ya está en Base.metadata, pero no hace daño
        # render_as_batch=True # Necesario para SQLite, opcional para otros
        compare_type=True, # Compara tipos de columnas al autogenerar
        naming_convention=target_metadata.naming_convention, # Usa nuestra convención
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Obtenemos la URL de la base de datos desde nuestra configuración
    db_url = get_database_url()

    # Creamos la configuración para el engine a partir de la URL
    connectable_config = config.get_section(config.config_ini_section, {})
    connectable_config["sqlalchemy.url"] = db_url # Establecemos la URL obtenida

    connectable = engine_from_config(
        connectable_config, # Usamos la config con nuestra URL
        prefix="sqlalchemy.",
        poolclass=pool.NullPool, # NullPool es recomendado para migraciones
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Añade la convención de nombres aquí también
            compare_type=True, # Compara tipos de columnas
            naming_convention=target_metadata.naming_convention, # Usa nuestra convención
            # render_as_batch=True # Necesario para SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

