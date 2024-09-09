from sentence_transformers import SentenceTransformer

# Cargamos el modelo desde la carpeta local
ruta_local_modelo = './model_embeding/'  # Asegúrate de que la ruta sea correcta
model = SentenceTransformer(ruta_local_modelo)

def generar_embedding(texto):
    # Convertimos el texto a un embedding usando el modelo local
    embedding = model.encode(texto)
    return embedding

x = "tester"
y = "testeando"

print(generar_embedding(x))
print(generar_embedding(y))
