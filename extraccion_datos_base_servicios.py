import mysql.connector
import os
import sys
from ftplib import FTP, error_perm
from Tele import send_msg
from datetime import datetime

def limpiar_carpeta_local(carpeta_local):
    for archivo in os.listdir(carpeta_local):
        if archivo.endswith(".txt"):
            os.remove(os.path.join(carpeta_local, archivo))
    print(f"Se han eliminado todos los archivos .txt de la carpeta: {carpeta_local}")

def eliminar_archivos_pequenos(carpeta_local, tamano_maximo_kb):
    for archivo in os.listdir(carpeta_local):
        archivo_path = os.path.join(carpeta_local, archivo)
        if os.path.getsize(archivo_path) < tamano_maximo_kb * 1024:
            # Actualizar estado en la base de datos antes de eliminar
            actualizar_estado_audio(archivo, 'error audio')
            os.remove(archivo_path)
            print(f"Archivo eliminado por ser menor a {tamano_maximo_kb} KB: {archivo} de {carpeta_local}")

def copiar_archivos_desde_ftp(archivos, carpeta_ftp, carpeta_local):
    ftp = FTP('192.168.50.37')
    ftp.login(user='rpaback1', passwd='Cyber123')
    ftp.cwd(carpeta_ftp)

    archivos_no_encontrados = []
    archivos_copiados = 0

    for archivo in archivos:
        try:
            with open(os.path.join(carpeta_local, archivo), 'wb') as f:
                ftp.retrbinary('RETR ' + archivo, f.write)
            archivos_copiados += 1
        except error_perm:
            print(f"Archivo no encontrado en el FTP: {archivo}")
            actualizar_estado_audio(archivo, 'not found txt')
            archivos_no_encontrados.append(archivo)

    ftp.quit()
    if carpeta_local == r'C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\chat':
        if archivos_no_encontrados:
            cantidad_no_encontrados = len(archivos_no_encontrados)
            # send_msg(f"Servicios, {cantidad_no_encontrados} audios no encontrados en el FTP.")
            print(f"Se han registrado {cantidad_no_encontrados} audios no encontrados.")

            fecha_hoy = datetime.now().strftime("%Y%m%d")
            ruta_no_encontrados = os.path.join(r'C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\registro no encontrados', f'audios_no_descargados_{fecha_hoy}.txt')

            with open(ruta_no_encontrados, 'a') as f:
                for archivo in archivos_no_encontrados:
                    f.write(f"{archivo}\n")

            print(f"Audios no encontrados registrados en: {ruta_no_encontrados}")

def actualizar_estado_audio(nombre_audio, estado):
    print("actualizando registros")
    try:
        nombre_audio_mp3 = nombre_audio.replace('.txt', '.mp3')
        
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="",
            database="audios_dana"
        )
        cursor = conexion.cursor()
        consulta_actualizacion = "UPDATE audios SET status = %s WHERE audio_name = %s"
        cursor.execute(consulta_actualizacion, (estado, nombre_audio_mp3))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("actualizados")
    except mysql.connector.Error as error:
        print(f"Error al actualizar el estado del audio {nombre_audio_mp3}: {error}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

conexion = mysql.connector.connect(
    host="192.168.51.210",
    user="root",
    password="",
    database="audios_dana"
)
cursor = conexion.cursor()
consulta = ("SELECT audio_name FROM audios WHERE owner = 'izzi' AND tipo = 'servicios' and status in ('Transcrito','Reprocesar') ORDER BY id DESC LIMIT 1")

try:
    cursor.execute(consulta)
    nombres_audios = cursor.fetchall()

    if not nombres_audios:
        print("No se encontraron audios")
        sys.exit(1)

    # Actualizar el estado de los audios a 'Procesando'
    for nombre_audio in nombres_audios:
        actualizar_estado_audio(nombre_audio[0], 'Procesando')

    nombres_audios_txt = [nombre_audio[0].replace('.mp3', '.txt') for nombre_audio in nombres_audios]

    carpeta_local_transcripciones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\transcripciones"
    limpiar_carpeta_local(carpeta_local_transcripciones)

    carpeta_ftp_transcripciones = "Transcripciones/Transcripciones/"
    num_transcripciones = copiar_archivos_desde_ftp(nombres_audios_txt, carpeta_ftp_transcripciones, carpeta_local_transcripciones)

    print(f"Se Guardaron los {num_transcripciones} transcripciones del ftp")

    carpeta_local_chat = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\chat"
    limpiar_carpeta_local(carpeta_local_chat)

    carpeta_ftp_chat = "Transcripciones/Chat/"
    num_chat = copiar_archivos_desde_ftp(nombres_audios_txt, carpeta_ftp_chat, carpeta_local_chat)

    print(f"Se Guardaron los {num_chat} chats del ftp")

    eliminar_archivos_pequenos(carpeta_local_transcripciones, .5)
    eliminar_archivos_pequenos(carpeta_local_chat, .5)

    sys.exit(0)
except mysql.connector.Error as error:
    print("Error al ejecutar la consulta:", error)
    send_msg("Error al ejecutar la consulta de Servicios Para Exctraer Audios:", error)
    sys.exit(2)
finally:
    cursor.close()
    conexion.close()
