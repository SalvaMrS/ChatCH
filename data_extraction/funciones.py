from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from typing import List, Tuple

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

def extraer_filas(imagen: np.ndarray) -> List[List[np.ndarray]]:
    """
    Divide una imagen de tabla en una lista de listas, donde cada sublista contiene dos celdas (imágenes).

    Args:
        imagen (np.ndarray): La imagen de la tabla.

    Returns:
        List[List[np.ndarray]]: Una lista de listas, donde cada sublista contiene dos imágenes correspondientes a las celdas.
    """
    filas = crop_image_by_lines(imagen)[1:-1]
    celdas_por_fila = [crop_image_by_lines(fila, False)[1:-1] for fila in filas]
    return [celdas for celdas in celdas_por_fila if len(celdas) == 2]

def insertar_fila_en_bd(collection, celdas: List[np.ndarray], idx: int) -> int:
    """
    Inserta en la base de datos una lista de celdas extraídas de una tabla.

    Args:
        collection: La colección de la base de datos donde se insertarán los datos.
        celdas (List[List[np.ndarray]]): Una lista de listas que contiene las celdas extraídas de la tabla.
        idx (int): Un identificador único para cada documento que se insertará en la colección.

    Returns:
        int: El nuevo índice actualizado después de la inserción.
    """
    for celda in celdas:
        enfermedad = img2txt(celda[0])
        data = img2txt(celda[1])
        collection.add(documents=[enfermedad], 
                        metadatas=[{"enfermedad": enfermedad, "data": data}], 
                        ids=[str(idx)])
        idx += 1
    return idx


def encontrar_puntos(texto: str) -> List[Tuple[str, int]]:
    patron = r'([A-Z]{1,2}) ?(\d{2})'
    return [(letras, int(numeros)) for letras, numeros in re.findall(patron, texto)]


if __name__ == "__main__":
    ruta = './databases/tratamientos/011-020.pdf'
    paginas = convert_from_path(ruta)
    lenfilas = 0

    for pagina in paginas:
        pagina = cv2.cvtColor(pagina, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
        filas = extraer_filas(pagina)
        for fila in filas:
            idx = insertar_fila_en_bd(None, fila, idx) # 37 filas

    print(lenfilas)
    