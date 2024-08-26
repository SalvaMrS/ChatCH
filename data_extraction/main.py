from funciones import *
import chromadb
import os

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

        pagina = cv2.cvtColor(np.array(pagina), cv2.COLOR_BGR2GRAY)
        filas = extraer_filas(pagina)
        for fila in filas:
            enf = img2txt(fila[0])
            palabras.update(re.findall(r'\b[A-Za-záéíóúÁÉÍÓÚñÑüÜ]+\b', enf))

            poin = img2txt(fila[1])

            collection.add(documents=[enf], 
                            metadatas=[{"enfermedad": enf, "data": poin}], 
                            ids=[str(idx)])
            idx += 1
        
with open('databases/enfermedades.txt', 'w', encoding='utf-8') as f:
    for palabra in palabras:
        f.write(palabra + '\n')

if __name__ == "__main__":
    print(collection.count())  # Imprime el conteo de documentos en la colección