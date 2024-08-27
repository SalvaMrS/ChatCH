from spellchecker import SpellChecker

def cargar_diccionario_medico(spell, archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        terminos_medicos = [linea.strip() for linea in f]
    spell.word_frequency.load_words(terminos_medicos)

def corregir_errores(frase):
    spell = SpellChecker(language='es')
    cargar_diccionario_medico(spell, 'databases/enfermedades.txt')

    palabras = frase.split()
    palabras_corregidas = [spell.correction(palabra) for palabra in palabras]
    frase_corregida = ' '.join(palabras_corregidas)
    return frase_corregida
