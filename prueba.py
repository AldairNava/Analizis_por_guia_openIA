import os

# Nombre de la carpeta donde se guardarán los archivos
carpeta_salida = r'C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\transcripciones'

# Crear la carpeta si no existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Lee la lista desde un archivo de texto
with open(r'C:\Users\Jotzi1\Desktop\AnalizandorMasivoMariana\audios.txt', 'r') as archivo:
    nombres = archivo.readlines()

# Elimina los saltos de línea y espacios en blanco al principio y final de cada nombre
nombres = [nombre.strip() for nombre in nombres]

# Crea un archivo .txt para cada nombre en la lista dentro de la carpeta especificada
for nombre in nombres:
    with open(os.path.join(carpeta_salida, f'{nombre}.txt'), 'w') as nuevo_archivo:
        nuevo_archivo.write(f"Este es el archivo {nombre}")

print(f"Archivos creados con éxito en la carpeta '{carpeta_salida}'.")
