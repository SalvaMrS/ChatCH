from funciones import *
from sentence_transformers import SentenceTransformer
import chromadb
import os

ruta_local_modelo = './model_embeding/'
model = SentenceTransformer(ruta_local_modelo)

# Configurar ChromaDB para usar SQLite como backend
client = chromadb.PersistentClient(path="./databases/chromadb")

# Crear o conectar a una colección
collection = client.get_or_create_collection(name="Enfermedades")

# Especifica el path de la carpeta
carpeta = './databases/tratamientos/'

archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]

idx = 0
palabras = set()
points = set()
for archivo in archivos:
    ruta = carpeta + archivo
    paginas = convert_from_path(ruta)

    for pagina in paginas:
        if __name__ == "__main__":
            print(idx)

        pagina = np.array(pagina)
        pagina = cv2.cvtColor(pagina, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
        idx = insertar_datos_paginas(collection, pagina, idx, model)

if __name__ == "__main__":
    print(collection.count())  # Imprime el conteo de documentos en la colección