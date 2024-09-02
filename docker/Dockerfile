# Usa una imagen base que soporte Python y los requerimientos de tu proyecto
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia las carpetas databases y web desde la raíz del repositorio al contenedor
COPY databases /app/databases
COPY web /app/web

# Copia el entorno virtual al contenedor
COPY venv /app/venv

# Define el comando por defecto que se ejecutará cuando inicie el contenedor
CMD ["/app/venv/bin/uvicorn", "web.API.main:app", "--reload", "--host", "0.0.0.0"]
