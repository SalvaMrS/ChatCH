from sentence_transformers import SentenceTransformer
import chromadb
from tabulate import tabulate
from spellchecker import SpellChecker

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

ruta_local_modelo = './model_embeding/'  # Asegúrate de que la ruta sea correcta
model = SentenceTransformer(ruta_local_modelo)

# Configurar el cliente ChromaDB
client = chromadb.PersistentClient(path="./databases/chromadb")
collection = client.get_collection(name="Enfermedades")

# Variable a buscar
buscar_str = input("Ingrese la enfermedad: ")

# Realizar la consulta
resultados = collection.query(
    query_embeddings=model.encode(buscar_str).tolist(),
    n_results=30  # Cambia el número de resultados según tus necesidades
)

table = []
# Agregar resultados a la tabla
for i in range(len(resultados['documents'][0])):
    enfermedad = resultados['documents'][0][i]
    data = resultados['metadatas'][0][i].get('data', 'No disponible')
    table.append([enfermedad, data]) 

print(tabulate(table, headers=["Enfermedad", "Data"], tablefmt="grid"))
