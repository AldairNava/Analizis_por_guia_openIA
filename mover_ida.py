import os
import shutil
import random

# Directorio de origen y destino
directorio_origen = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\audios_extraidos'
directorio_destino = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\audios'

# Lista de archivos de audio en el directorio de origen
archivos_audio = [archivo for archivo in os.listdir(directorio_origen) if archivo.endswith('.mp3') or archivo.endswith('.wav')]

# Escoger 30 archivos aleatorios si hay más de 30 archivos de audio
if len(archivos_audio) > 30:
    archivos_a_mover = random.sample(archivos_audio, 30)
else:
    archivos_a_mover = archivos_audio

# Mover los archivos seleccionados al directorio de destino
for archivo in archivos_a_mover:
    ruta_origen = os.path.join(directorio_origen, archivo)
    ruta_destino = os.path.join(directorio_destino, archivo)
    shutil.move(ruta_origen, ruta_destino)
    print(f"Se ha movido el archivo {archivo} a {directorio_destino}")
