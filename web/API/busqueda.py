import chromadb
from tabulate import tabulate

# Configurar el cliente ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="Enfermedades")

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


print(tabulate(data, headers=["Enfermedad", "Data"], tablefmt="grid"))