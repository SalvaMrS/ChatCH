from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import pytesseract
from funciones import *
import chromadb

def img2txt(img):
    pil_img = Image.fromarray(img)

    texto = pytesseract.image_to_string(pil_img)

    return texto

PDF_PATH = "../test.pdf"
idx = 0

# Configurar ChromaDB para usar SQLite como backend
client = chromadb.PersistentClient(path="./db")

# Crear o conectar a una colección
collection = client.get_or_create_collection(name="Enfermedades")

paginas = convert_from_path(PDF_PATH)

for pag in paginas: 
    image = np.array(pag)

    filas = crop_image_by_heights(image)

    for fila in filas:
        celdas = crop_image_by_widths(fila)

        enfermedad = img2txt(celdas[0])

        info = img2txt(celdas[1])

        collection.add(documents=[enfermedad], metadatas=[{"enfermedad": enfermedad, "info": info}], ids=[idx])

        idx += 1
       
