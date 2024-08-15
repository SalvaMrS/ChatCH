from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import pytesseract

def display_image(image):
    if isinstance(image, Image.Image):
        image = np.array(image)

    cv2.imshow('Image', image)
    cv2.waitKey(5000)   
    cv2.destroyAllWindows()

def detect_line(image: np.ndarray, horizontal: bool = True) -> list[int]:
    """
    Detecta las filas o columnas menos brillantes en una imagen y devuelve sus índices.

    Args:
        image (np.ndarray): La imagen en la que se evaluarán las filas o columnas. 
                            Debe ser una imagen en formato BGR.
        horizontal (bool): Indica si se deben evaluar filas (True) o columnas (False).

    Returns:
        list[int]: Una lista de índices correspondientes al 25% de las filas o columnas menos brillantes.
    """
    
    # Suma los valores de los píxeles a lo largo de las filas o columnas
    brightness_sums = np.sum(image, axis=1 if horizontal else 0)

    
    # Calcula el valor del percentil 
    threshold = np.percentile(brightness_sums, 0.1)
    
    # Selecciona los índices donde el brillo es menor o igual al percentil
    darkest_indices = np.where(brightness_sums <= threshold)[0]
    
    return darkest_indices.tolist()


def crop_image_by_lines(image: np.ndarray, horizontal: bool = True) -> list[np.ndarray]:
    """
    Recorta una imagen en secciones basadas en líneas detectadas.

    Args:
        image (np.ndarray): La imagen que se va a recortar. Debe ser un arreglo de numpy 
                            representando la imagen en formato BGR.
        horizontal (bool): Indica si el recorte se debe realizar por líneas horizontales 
                           (True) o verticales (False). Por defecto es True.

    Returns:
        list[np.ndarray]: Una lista de imágenes recortadas. Si no se detectan líneas, 
                          se devuelve una lista vacía.
    """
    cropped_images = []
    dimension = image.shape[0] if horizontal else image.shape[1]  # Obtiene la dimensión correspondiente

    lines = sorted(set(detect_line(image, horizontal)))
    lines.append(dimension)

    # Recortar la imagen según las líneas
    start = 0

    for line in lines:
        finish = min(line, dimension)  # Define el límite de recorte

        if start + 2 < finish:  # Asegúrate de que hay suficiente espacio para recortar
            if horizontal:
                cropped_image = image[start + 2:finish]  # Recorta la imagen por filas
            else:
                cropped_image = image[:, start + 2:finish]  # Recorta la imagen por columnas

            if cropped_image.shape[0 if horizontal else 1] > 10:  # Solo agregar si tiene dimensión
                cropped_images.append(cropped_image)

        start = finish + 1

    return cropped_images



def img2txt(img: np.ndarray) -> str:
    """
    Convierte una imagen en texto utilizando OCR (Reconocimiento Óptico de Caracteres).

    Args:
        img (np.ndarray): La imagen de entrada en formato de arreglo de numpy, 
                          que debe ser en escala de grises o en color.

    Returns:
        str: El texto extraído de la imagen. Si no se puede extraer texto, 
             se devuelve una cadena vacía.
    """
    pil_img = Image.fromarray(img)  # Convierte el arreglo de numpy a una imagen PIL

    texto = pytesseract.image_to_string(pil_img)  # Extrae el texto de la imagen usando Tesseract OCR

    return texto


def insertar_datos_paginas(collection, pagina, idx: int) -> None:
    """
    Inserta datos extraídos de un archivo PDF en una colección de base de datos.

    Args:
        collection: La colección de la base de datos donde se insertarán los datos.
                    Debe tener un método `add` para agregar documentos.
        path_pdf (str): La ruta al archivo PDF del cual se extraerán los datos.
        idx (int): Un identificador único para cada documento que se insertará en la colección.

    Returns:
        None: Esta función no retorna ningún valor. Los datos se insertan directamente en la colección.
    """

    image = np.array(pagina)  # Convierte la imagen de la página a un arreglo de numpy

    filas = crop_image_by_lines(image)[1:-1]  # Recorta la imagen en líneas y elimina la primera y última

    for fila in filas:
        celdas = crop_image_by_lines(fila, False)[1:-1]  # Recorta la fila en celdas y elimina la primera y última

        if len(celdas) != 2:  # Verifica que haya exactamente dos celdas
            continue  # Si no, continúa con la siguiente fila

        if not collection:
            global lenfilas
            lenfilas += 1

            continue

        enfermedad = img2txt(celdas[0])  # Extrae el texto de la primera celda (enfermedad)

        data = img2txt(celdas[1])  # Extrae el texto de la segunda celda (data)


        # Agrega el documento a la colección con la enfermedad y los datos extraídos
        collection.add(documents=[enfermedad], 
                        metadatas=[{"enfermedad": enfermedad, "data": data}], 
                        ids=[str(idx)])
        idx += 1
               
    return idx 



if __name__ == "__main__":
    ruta = './databases/tratamientos/011-020.pdf'
    paginas = convert_from_path(ruta)
    lenfilas = 0

    for pagina in paginas:
        pagina = cv2.cvtColor(pagina, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
        insertar_datos_paginas(None, pagina, 0) # 37 filas

    print(lenfilas)
    