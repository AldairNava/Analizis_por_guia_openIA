import mysql.connector
import os
import sys
from ftplib import FTP, error_perm, error_temp, error_proto
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
    try:
        ftp = FTP('192.168.50.37')
        ftp.login(user='rpaback1', passwd='Cyber123')
        ftp.cwd(carpeta_ftp)
    except (error_temp, error_proto) as e:
        print(f"Error de conexión al FTP: {e}")
        return 0
    except Exception as e:
        print(f"Error inesperado al intentar conectarse al FTP: {e}")
        send_msg(f'Error al Conectarce al FTP : {e}')
        return 0

    archivos_no_encontrados = []
    archivos_copiados = 0

    # Determina si es transcripcion o chat por la carpeta de destino
    if 'transcripcion' in carpeta_local.lower():
        columna_bd = 'transcripcion'
    elif 'chat' in carpeta_local.lower():
        columna_bd = 'chat'
    else:
        columna_bd = None

    for archivo in archivos:
        path_local = os.path.join(carpeta_local, archivo)
        try:
            with open(path_local, 'wb') as f:
                ftp.retrbinary('RETR ' + archivo, f.write)
            archivos_copiados += 1
        except error_perm:
            print(f"Archivo no encontrado en el FTP: {archivo}")
            # Intenta buscar el texto en la base y guardarlo como txt
            if columna_bd:
                texto = obtener_texto_desde_bd(archivo, columna_bd)
                if texto:
                    with open(path_local, 'w', encoding='utf-8') as f:
                        f.write(texto)
                    archivos_copiados += 1
                    print(f"Archivo recuperado desde la base y guardado: {archivo}")
                else:
                    print(f"No encontrado ni en FTP ni en BD: {archivo}")
                    actualizar_estado_audio(archivo, 'not found txt')
                    archivos_no_encontrados.append(archivo)
            else:
                print(f"No se pudo determinar la columna para buscar {archivo}")
                actualizar_estado_audio(archivo, 'not found txt')
                archivos_no_encontrados.append(archivo)
        except Exception as e:
            print(f"Error inesperado al descargar el archivo {archivo}: {e}")

    try:
        ftp.quit()
    except Exception as e:
        print(f"Error al cerrar la conexión con el FTP: {e}")

    if archivos_no_encontrados and 'chat' in carpeta_local.lower():
        cantidad_no_encontrados = len(archivos_no_encontrados)
        print(f"Se han registrado {cantidad_no_encontrados} audios no encontrados.")
        fecha_hoy = datetime.now().strftime("%Y%m%d")
        ruta_no_encontrados = os.path.join(
            r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\registro no encontrados',
            f'audios_no_descargados_{fecha_hoy}.txt'
        )
        with open(ruta_no_encontrados, 'a') as f:
            for archivo in archivos_no_encontrados:
                f.write(f"{archivo}\n")
        print(f"Audios no encontrados registrados en: {ruta_no_encontrados}")




def obtener_texto_desde_bd(nombre_txt, columna):
    try:
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )
        cursor = conexion.cursor()
        nombre_mp3 = nombre_txt.replace('.txt', '.mp3')
        consulta = f"SELECT {columna} FROM transcripcionesAudios WHERE filename = %s"
        cursor.execute(consulta, (nombre_mp3,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado and resultado[0]:
            return resultado[0]
        else:
            return None
    except Exception as e:
        print(f"Error consultando la base para {nombre_txt} columna {columna}: {e}")
        return None
def actualizar_estado_audio(nombre_audio, estado):
    print("actualizando registros")
    try:
        nombre_audio_mp3 = nombre_audio.replace('.txt', '.mp3')
        
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
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
    password="thor",
    database="audios_dana"
)
cursor = conexion.cursor()
consulta = ("SELECT audio_name FROM audios WHERE tipo = 'soporte' and status in ('Transcrito','Reprocesar') and guia = 'guia_set_9' ORDER BY id ASC LIMIT 1")

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

    carpeta_local_transcripciones = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones"
    limpiar_carpeta_local(carpeta_local_transcripciones)

    carpeta_ftp_transcripciones = "Transcripciones/Transcripciones/"
    num_transcripciones = copiar_archivos_desde_ftp(nombres_audios_txt, carpeta_ftp_transcripciones, carpeta_local_transcripciones)

    print(f"Se Guardaron los {num_transcripciones} transcripciones del ftp")

    carpeta_local_chat = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\chat"
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
