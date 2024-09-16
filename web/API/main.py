from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import chromadb
from .funciones import corregir_errores
from pathlib import Path
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Servir archivos estáticos desde el directorio 'web'
app.mount("/images", StaticFiles(directory="web/images"), name="images")

# Especificar la ruta al modelo en la raíz del proyecto
ruta_local_modelo = './model_embeding/'  # Asegúrate de que la ruta sea correcta
model = SentenceTransformer(ruta_local_modelo)

client = chromadb.PersistentClient(path="./databases/chromadb")
collection = client.get_collection(name="Enfermedades")

class QueryModel(BaseModel):
    query_text: str

# Diccionario para almacenar resultados de búsqueda
search_results = {}

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = Path("./web/base.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)

@app.post("/search")
async def search(query: QueryModel):
    corregido = corregir_errores(query.query_text)
    resultados = collection.query(query_embeddings=model.encode(corregido).tolist(), n_results=10)

    documentos = resultados.get('documents', [])[0]
    metadatas = resultados.get('metadatas', [])[0]

    # Rehacer el diccionario en cada búsqueda
    global search_results
    search_results = {}

    # Guarda los resultados en el diccionario 'search_results' usando enumerate como ID
    for i, doc in enumerate(documentos):
        enfermedad = f"{i}. {doc}"  # Crea una clave única con el índice de enumerate
        search_results[enfermedad] = metadatas[i].get('data', 'No disponible') if i < len(metadatas) else 'No disponible'

    # Devuelve los resultados con el ID (basado en enumerate)
    results = [{'enfermedad': f"{i}. {doc}", 'index': i} for i, doc in enumerate(documentos)]
    return {"results": results}

@app.get("/details")
async def get_details(query_text: str):
    # Busca el nombre completo de la enfermedad en el diccionario
    details = search_results.get(query_text, "Tratamiento no encontrado")

    return {"details": details}

