# backend/Procfile
# web: Comando para iniciar el servidor web
# $PORT es una variable de entorno que Heroku asigna automáticamente
# app.main:app -> Le dice a uvicorn dónde encontrar tu instancia FastAPI
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
# -w 4: Número de workers (ajusta según tu plan de Heroku, 2-4 es común para empezar)
# -k uvicorn.workers.UvicornWorker: Usa workers de Uvicorn para manejar ASGI
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --preload

# release: Comando para ejecutar durante la fase de despliegue (después de construir, antes de lanzar)
# Aquí ejecutamos las migraciones de Alembic
release: alembic upgrade head
