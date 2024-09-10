# Usa una imagen base que soporte Python y los requerimientos de tu proyecto
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia las carpetas databases y web desde la raíz del repositorio al contenedor
COPY ./databases /app/databases
COPY ./web /app/web

# Copia el archivo de requerimientos
COPY ./requirements.txt /app/requirements.txt

# Instala virtualenv y crea un entorno virtual dentro del contenedor
RUN python3 -m venv /app/venv

# Activa el entorno virtual e instala las dependencias
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r /app/requirements.txt

# Define el comando por defecto que se ejecutará cuando inicie el contenedor
CMD ["/app/venv/bin/uvicorn", "web.API.main:app", "--host", "0.0.0.0"]
