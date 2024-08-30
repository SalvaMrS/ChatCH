# Usa una imagen base que soporte Python y los requerimientos de tu proyecto
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt desde la raíz del repositorio al contenedor
COPY ../requirements.txt /app/requirements.txt

# Copia las carpetas databases y web desde la raíz del repositorio al contenedor
COPY ../databases /app/databases
COPY ../web /app/web

# Instala las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Define el comando por defecto que se ejecutará cuando inicie el contenedor
CMD ["uvicorn", "web.API.main:app", "--reload", "--host", "0.0.0.0"]
