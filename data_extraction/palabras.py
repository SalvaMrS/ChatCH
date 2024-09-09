import chromadb
import re

def extract_unique_words_from_chromadb(db_path, collection_name, output_file):
    # Conectar con la base de datos ChromaDB
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name=collection_name)

    # Recuperar todos los documentos y metadatos
    all_data = collection.get(include=["documents"])

    # Extraer todos los documentos
    documents = all_data["documents"]

    # Crear un set para almacenar palabras únicas
    unique_words = set()

    # Expresión regular para extraer palabras (sin números y separados por caracteres especiales)
    word_pattern = re.compile(r'\b[A-Za-z]+(?:\'[A-Za-z]+)?\b')

    # Procesar cada documento
    for doc in documents:
        words = word_pattern.findall(doc)  # Encontrar todas las palabras según el patrón
        unique_words.update(word.lower() for word in words)  # Añadir las palabras al set en minúsculas

    # Guardar las palabras únicas en el archivo
    with open(output_file, 'w') as file:
        for word in sorted(unique_words):
            file.write(f"{word}\n")

    print(f"Palabras únicas guardadas en {output_file}")

# Usar la función
extract_unique_words_from_chromadb(db_path="./databases/chromadb/", collection_name="Enfermedades", output_file="./databases/enfermedades.txt")
