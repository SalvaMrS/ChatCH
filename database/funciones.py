from pdf2image import convert_from_path
import cv2
import numpy as np

def display_image(image):
    cv2.imshow('Image', image)
    cv2.waitKey(5000)   
    cv2.destroyAllWindows()

def detect_horizontal_lines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 700)

    heights = []
    
    if lines is None:
        return heights

    for line in lines:
        rho, theta = line[0]
        if np.abs(theta - np.pi / 2) < 1e-5 or np.abs(theta - 3 * np.pi / 2) < 1e-5:  # Check for perfectly horizontal lines
            heights.append(int(rho))  # Guardar la altura de la línea

    return heights

def crop_image_by_heights(image):
    cropped_images = []
    height = image.shape[0]

    # Asegúrate de que las alturas estén ordenadas
    heights = detect_horizontal_lines(image)

    # Recortar la imagen según las alturas
    start = 0
    for h in heights:
        if h > start:
            cropped_image = image[start + 2:h]
            if cropped_image.shape[0] > 0:  # Solo agregar si tiene dimensión
                cropped_images.append(cropped_image)
        start = h + 1  # Saltar la línea

    # Recortar desde la última altura hasta el final de la imagen
    if start < height:
        cropped_image = image[start:height]
        if cropped_image.shape[0] > 0:  # Solo agregar si tiene dimensión
            cropped_images.append(cropped_image)

    # Eliminar la primera y última imagen
    return cropped_images[1:-1]


def detect_vertical_lines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 300)

    widths = []
    
    if lines is None:
        return widths

    for line in lines:
        rho, theta = line[0]
        if np.abs(theta) < 1e-5 or np.abs(theta - np.pi) < 1e-5:  # Check for perfectly vertical lines
            widths.append(int(rho))  # Guardar la posición de la línea

    return widths

def crop_image_by_widths(image):
    cropped_images = []
    width = image.shape[1]

    # Asegúrate de que las anchuras estén ordenadas
    widths = detect_vertical_lines(image)

    # Recortar la imagen según las anchuras
    start = 0
    for w in widths:
        if w > start:
            cropped_image = image[:, start + 2:w]  # Recortar por columnas
            if cropped_image.shape[1] > 0:  # Solo agregar si tiene dimensión
                cropped_images.append(cropped_image)
        start = w + 1  # Saltar la línea

    # Recortar desde la última altura hasta el final de la imagen
    if start < width:
        cropped_image = image[:, start + 2:width]
        if cropped_image.shape[1] > 0:  # Solo agregar si tiene dimensión
            cropped_images.append(cropped_image)

    # Eliminar la primera y última imagen
    return cropped_images[1:-1]
