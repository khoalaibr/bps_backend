# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # Importa la configuración con DATABASE_URL

# Crea el motor (engine) de SQLAlchemy usando la URL de la base de datos
# pool_pre_ping=True verifica las conexiones antes de usarlas, lo cual es bueno
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

# Crea una fábrica de sesiones (SessionLocal) configurada
# autocommit=False y autoflush=False son configuraciones estándar para FastAPI
# Se prefiere manejar las transacciones explícitamente (commit/rollback)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos (dependencia para FastAPI)
def get_db():
    """
    Generador de dependencia que proporciona una sesión de base de datos
    por cada solicitud y la cierra automáticamente al finalizar.
    """
    db = SessionLocal()
    try:
        yield db # Proporciona la sesión a la ruta
    finally:
        db.close() # Cierra la sesión al terminar la solicitud
