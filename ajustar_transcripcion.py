import os
import re

def eliminar_etiquetas(texto):

    patron = r'\b[ABCDEFGHI]:\s'
    
    texto_sin_etiquetas = re.sub(patron, '', texto)
    return texto_sin_etiquetas

def procesar_archivo(ruta_archivo):
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    contenido_procesado = eliminar_etiquetas(contenido)
    print(contenido_procesado)

    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido_procesado)

carpeta = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

for nombre_archivo in os.listdir(carpeta):
    
    if nombre_archivo.endswith('.txt'):
        
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        
        procesar_archivo(ruta_completa)
