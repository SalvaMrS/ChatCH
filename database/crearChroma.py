import chromadb

# Configurar ChromaDB para usar SQLite como backend
client = chromadb.PersistentClient(path="./db")

# Crear o conectar a una colección
collection = client.get_or_create_collection(name="mi_coleccion")

# Agregar datos de ejemplo a la colección
documents = ["lorem ipsum", "doc2", "doc3"]
metadatas = [{"chapter": "1"}, {"chapter": "2"}, {"chapter": "3"}]
ids = ["id1", "id2", "id3"]

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print("Base de datos SQLite creada y datos agregados.")