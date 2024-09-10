import os
import re
import PyPDF2

# Función para extraer el texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Función para separar las palabras de un texto (excluyendo números y separando por caracteres especiales)
def extract_words_from_text(text):
    # Expresión regular ajustada para incluir caracteres acentuados y la ñ, excluyendo números
    word_pattern = re.compile(r'\b[áéíóúüñÁÉÍÓÚÜÑa-zA-Z]+\b', re.UNICODE)
    words = word_pattern.findall(text)
    return set(word.lower() for word in words)

# Función principal para iterar sobre los PDFs de la carpeta, extraer texto y palabras únicas
def process_pdfs_in_folder(folder_path):
    unique_words = set()

    # Iterar sobre todos los archivos PDF en la carpeta
    for file_name in os.listdir(folder_path):
        pdf_path = os.path.join(folder_path, file_name)
        print(f"Procesando archivo: {pdf_path}")
        
        # Extraer texto del PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Extraer palabras únicas del texto
        words = extract_words_from_text(text)
        unique_words.update(words)

    return unique_words

# Función para guardar palabras únicas en un archivo de texto
def save_unique_words_to_file(words, output_file):
    with open(output_file, 'w') as file:
        for word in sorted(words):
            file.write(f"{word}\n")
    print(f"Palabras únicas guardadas en {output_file}")

# Usar la función para procesar los PDFs en la carpeta ./databases/tratamientos
unique_words = process_pdfs_in_folder("./databases/tratamientos/")
save_unique_words_to_file(unique_words, "./databases/enfermedades.txt")
