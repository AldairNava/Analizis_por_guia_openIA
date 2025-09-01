import os
import mysql.connector
from datetime import datetime, timedelta

def status_completado():
    print("\nINICIANDO STATUS DE COMPLETADO\n")
    
    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    cursor = conexion.cursor()

    # Obtener los últimos 10 días
    fecha_actual = datetime.now()
    fecha_inicio = (fecha_actual - timedelta(days=10)).strftime('%Y-%m-%d')
    print(f"Fecha actual: {fecha_actual}")
    print(f"Fecha de inicio: {fecha_inicio}")

    # Consulta para obtener registros desde los últimos 10 días
    consulta_select = """
    SELECT audio_name, status 
    FROM audios 
    WHERE date(created_at) >= %s
    """
    cursor.execute(consulta_select, (fecha_inicio,))
    registros_audios = cursor.fetchall()
    # print("Registros obtenidos de la base de datos:", registros_audios)

    nombres_archivo_existente = {registro[0]: registro[1] for registro in registros_audios}
    # print("Nombres de archivo existentes:", nombres_archivo_existente)

    carpeta_transcripcion = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov4'
    print(f"Carpeta de transcripción: {carpeta_transcripcion}")

    for archivo in os.listdir(carpeta_transcripcion):
        nombre_archivo, extension = os.path.splitext(archivo)
        nombre_archivo_mp3 = nombre_archivo + ".mp3"
        print(f"Procesando archivo: {archivo}, nombre de archivo mp3: {nombre_archivo_mp3}")

        if nombre_archivo_mp3 in nombres_archivo_existente:
            estado_actual = nombres_archivo_existente[nombre_archivo_mp3]
            print(f"Estado actual de {nombre_archivo_mp3}: {estado_actual}")
            if estado_actual != 'Audio de baja calidad':
                consulta = "UPDATE audios SET status = 'Completado', analizado_tareas = 1, analyzed = 1 WHERE audio_name = %s"
                cursor.execute(consulta, (nombre_archivo_mp3,))
                print(f"Se ha actualizado el registro: {nombre_archivo_mp3}")

                # Actualizar en la otra tabla
                consulta_prueba_dana_calidad = """
                UPDATE prueba_dana_calidad
                SET 
                    transcripcion = TO_BASE64(AES_ENCRYPT(transcripcion, '4:1+%iP.Km3@e5Lt')),
                    chat = TO_BASE64(AES_ENCRYPT(chat, '4:1+%iP.Km3@e5Lt')),
                    transcripcion_original = TO_BASE64(AES_ENCRYPT(transcripcion_original, '4:1+%iP.Km3@e5Lt'))
                WHERE 
                    filename = %s
                """
                cursor.execute(consulta_prueba_dana_calidad, (nombre_archivo_mp3,))
                print(f"También se ha actualizado en la tabla prueba_dana_calidad: {nombre_archivo_mp3}")

    conexion.commit()
    cursor.close()
    conexion.close()
    print("\nPROCESO COMPLETADO\n")

if __name__ == "__main__":
    status_completado()
