import os
import mysql.connector
from datetime import datetime

def status_completado():
    print("\nINICIANDO STATUS DE COMPLETADO")
    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    cursor = conexion.cursor()


    # Obtener el primer día del mes actual
    fecha_actual = datetime.now()
    primer_dia_mes = fecha_actual.replace(day=1).strftime('%Y-%m-%d')

    # Consulta para obtener registros desde el primer día del mes actual
    consulta_select = """
    SELECT audio_name, status 
    FROM audios 
    WHERE date(created_at) >= %s
    """
    cursor.execute(consulta_select, (primer_dia_mes,))
    registros_audios = cursor.fetchall()

    nombres_archivo_existente = {registro[0]: registro[1] for registro in registros_audios}

    carpeta_transcripcion = r'C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\calificacion\pov4'

    for archivo in os.listdir(carpeta_transcripcion):
        nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"

        if nombre_archivo in nombres_archivo_existente:
            estado_actual = nombres_archivo_existente[nombre_archivo]
            if estado_actual != 'Audio de baja calidad':
                consulta = "UPDATE audios SET analyzed = 1, status = 'Completado', analizado_tareas = 1 WHERE audio_name = %s"
                cursor.execute(consulta, (nombre_archivo,))
                print(f"Se ha actualizado el registro: {nombre_archivo}")
                
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
                cursor.execute(consulta_prueba_dana_calidad, (nombre_archivo,))
                print(f"También se ha actualizado en la tabla prueba_dana_calidad: {nombre_archivo}")

    conexion.commit()
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    status_completado()
