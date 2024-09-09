import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np
import chromadb
from tabulate import tabulate

# Configurar el cliente ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="Enfermedades")
from spellchecker import SpellChecker

class ONNXEmbeddingFunction:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.session = ort.InferenceSession(model_path)

    def __call__(self, texts: list):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        input_ids = inputs["input_ids"].numpy()
        attention_mask = inputs["attention_mask"].numpy()
        
        # Perform inference
        outputs = self.session.run(None, {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        })
        
        # Assuming the model output is the embeddings
        embeddings = outputs[0]  # Change the index if necessary

        return embeddings

def cargar_diccionario_medico(spell, archivo):
    # Leer términos médicos del archivo
    with open(archivo, 'r', encoding='utf-8') as f:
        terminos_medicos = [linea.strip() for linea in f]
    spell.word_frequency.load_words(terminos_medicos)

def corregir_errores(frase):
    spell = SpellChecker(language='es')
    cargar_diccionario_medico(spell, 'databases/enfermedades.txt')

    palabras = frase.split()
    palabras_corregidas = [spell.correction(palabra) for palabra in palabras]
    frase_corregida = ' '.join(palabras_corregidas)
    return frase_corregida

# Ruta al directorio del modelo ONNX
model_path = "./all-MiniLM-L6-L6-v2/onnx/model.onnx"
tokenizer_path = "./all-MiniLM-L6-v2/onnx"

# Configurar la función de embedding con el modelo ONNX
embedding_function = ONNXEmbeddingFunction(model_path, tokenizer_path)

# Configurar el cliente ChromaDB
client = chromadb.PersistentClient(path="./databases/chromadb")
collection = client.get_collection(name="Enfermedades", embedding_function=embedding_function)

# Variable a buscar
buscar_str = input("Ingrese la enfermedad: ")

# Realizar la consulta
resultados = collection.query(
    query_texts=[buscar_str],
    n_results=5  # Cambia el número de resultados según tus necesidades
)

table = []
# Agregar resultados a la tabla
for i in range(len(resultados['documents'][0])):
    enfermedad = resultados['documents'][0][i]
    data = resultados['metadatas'][0][i].get('data', 'No disponible')
    table.append()

print(tabulate(table, headers=["Enfermedad", "Data"], tablefmt="grid"))
