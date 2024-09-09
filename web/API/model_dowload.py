from sentence_transformers import SentenceTransformer

# Descargamos y guardamos el modelo en una carpeta local
ruta_local_modelo = './model_embeding/'  # Reemplaza con la ruta que prefieras
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
model.save(ruta_local_modelo)
