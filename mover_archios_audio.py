import os
import shutil

# Rutas de las carpetas y del archivo de texto
ruta_txt = r'C:\Users\Jotzi1\Desktop\AnalizandorMasivoMariana\audios.txt'
carpeta_origen = r'C:\Users\Jotzi1\Desktop\AnalizandorMasivoMariana\archivos_audio'
carpeta_destino = r'C:\Users\Jotzi1\Desktop\AnalizandorMasivoMariana\archivos_encontrados'

# Leer los nombres de los archivos desde el archivo de texto
with open(ruta_txt, 'r', encoding='utf-8') as f:
    lista_archivos = f.read().splitlines()

# Crear la carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Mover los archivos que coinciden con los nombres en la lista
for nombre_archivo in lista_archivos:
    ruta_origen = os.path.join(carpeta_origen, nombre_archivo)
    ruta_destino = os.path.join(carpeta_destino, nombre_archivo)

    # Verificar si el archivo existe en la carpeta de origen
    if os.path.exists(ruta_origen):
        shutil.move(ruta_origen, ruta_destino)
        print(f'Archivo movido: {nombre_archivo}')
    else:
        print(f'Archivo no encontrado: {nombre_archivo}')
