from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import chromadb
from .funciones import corregir_errores
from pathlib import Path

app = FastAPI()

# Servir archivos estáticos desde el directorio 'web'
app.mount("/images", StaticFiles(directory="web/images"), name="images")

client = chromadb.PersistentClient(path="./databases/chromadb")
collection = client.get_collection(name="Enfermedades")

class QueryModel(BaseModel):
    query_text: str

search_results = {}

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = Path("./web/base.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_content)

@app.post("/search")
async def search(query: QueryModel):
    corregido = corregir_errores(query.query_text)
    resultados = collection.query(query_texts=[corregido], n_results=10)

    documentos = resultados.get('documents', [])[0]
    metadatas = resultados.get('metadatas', [])[0]

    global search_results
    search_results = {doc: metadatas[i].get('data', 'No disponible') if i < len(metadatas) else 'No disponible' for i, doc in enumerate(documentos)}

    results = [{'enfermedad': doc, 'data': search_results[doc]} for doc in search_results]
    return {"results": results}

@app.get("/details")
async def get_details(query_text: str):
    details = search_results.get(query_text, "Tratamiento no encontrado")
    return {"details": details}
