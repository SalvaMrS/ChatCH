from pdf2image import convert_from_path
import cv2
import numpy as np

from funciones import *


PDF_PATH = "../test.pdf"

paginas = convert_from_path(PDF_PATH)

for pag in paginas: 
    image = np.array(pag)

    filas = crop_image_by_heights(image)

    for fila in filas:
        celdas = crop_image_by_widths(fila)

        for celda in celdas:
            display_image(celda)
