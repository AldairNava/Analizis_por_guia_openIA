print("\n--------- INICIA CARGA MASIVA DE BASE DE DATOS ---------\n")

import sys
import re
import mysql.connector
import os

#cliente insatisfecho

def cliente_insatisfecho_cargar():
    carpeta_calificaciones = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\insatisfaccion'
    archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_calificaciones:
        ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
        filename = os.path.splitext(archivo)[0] + ".mp3"

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            respuesta = archivo.read()

        resultado = re.search(r'\d+', respuesta)

        if resultado:
            valor_satisfaccion = resultado.group(0)
            consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
            cursor.execute(consulta_existencia, (filename,))
            resultado_base = cursor.fetchone()

            if resultado_base[0] > 0:
                consulta = "UPDATE prueba_dana_calidad SET Cliente_insatisfecho = %s WHERE filename = %s"
                valores = (valor_satisfaccion, filename)
                cursor.execute(consulta, valores)
                print("La insatisfacción del archivo {} ha sido actualizada en la base de datos.".format(filename))
            else:
                print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))
        else:
            print(f"No se encontró ninguna indicación de satisfacción del cliente en el archivo '{archivo}'.")

    conexion.commit()
    cursor.close()
    conexion.close()

#cargar motivo llamada

import os
import mysql.connector

def cargar_motivo_problematica_sentimientos_solucion(guia, tipo):
    ruta_solucion = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\solucion"
    ruta_motivo = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\motivo_llamada"
    ruta_sentimientos = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\sentimientos"
    ruta_problematica = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\problematica"
    ruta_datos_actualizacion = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\datos_actualizcion"
    ruta_titularidad = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\titularidad"

    archivos_motivo = [f for f in os.listdir(ruta_motivo) if f.endswith('.txt')]

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_motivo:
        filename = os.path.splitext(archivo)[0] + ".mp3"

        rutas_archivos = {
            "Motivo_llamada": os.path.join(ruta_motivo, archivo),
            "Solucion": os.path.join(ruta_solucion, archivo),
            "Emociones_cliente": os.path.join(ruta_sentimientos, archivo),
            "Problematica": os.path.join(ruta_problematica, archivo),
            "Datos_actualizacion": os.path.join(ruta_datos_actualizacion, archivo),
            "Titular": os.path.join(ruta_titularidad, archivo)
        }

        contenido_archivos = {}

        for campo, ruta in rutas_archivos.items():
            if os.path.exists(ruta):
                with open(ruta, 'r', encoding='utf-8') as file:
                    contenido_archivos[campo] = file.read()
            else:
                print(f"Advertencia: El archivo {ruta} no existe. El campo {campo} no será actualizado.")
                contenido_archivos[campo] = None

        consulta_existencia = "SELECT COUNT(*) FROM audios WHERE audio_name = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado_base = cursor.fetchone()

        if resultado_base[0] > 0:
            consulta = """
            UPDATE audios SET 
                Motivo_llamada = %s, 
                Solucion = %s, 
                Emociones_cliente = %s, 
                Problematica = %s,
                Datos_actualizacion = %s,
                Titular = %s,
                owner = 'izzi',
                tipo = %s
            WHERE audio_name = %s"""
            valores = (
                contenido_archivos.get("Motivo_llamada"),
                contenido_archivos.get("Solucion"),
                contenido_archivos.get("Emociones_cliente"),
                contenido_archivos.get("Problematica"),
                contenido_archivos.get("Datos_actualizacion"),
                contenido_archivos.get("Titular"),
                tipo,
                filename
            )
            cursor.execute(consulta, valores)
            print("Los detalles del archivo {} han sido actualizados en la base de datos.".format(filename))
            
            # Actualizar la tabla de calificaciones dinámica
            consulta_calificaciones = f"""
            UPDATE calificaciones_{guia} SET 
                problematica = %s, 
                solucion = %s,
                owner = 'izzi',
                tipo = %s
            WHERE filename = %s"""
            valores_calificaciones = (
                contenido_archivos.get("Problematica"),
                contenido_archivos.get("Solucion"),
                tipo,
                filename
            )
            cursor.execute(consulta_calificaciones, valores_calificaciones)
            print("Los detalles del archivo {} han sido actualizados en la tabla calificaciones_{}.".format(filename, guia))
        else:
            print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))

    conexion.commit()
    cursor.close()
    conexion.close()



#cliente reincidencia

def reincidencia_cargar():
    carpeta_calificaciones = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\reincidencia'
    archivos_calificaciones = [f for f in os.listdir(carpeta_calificaciones) if f.endswith('.txt')]

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    cursor = conexion.cursor()

    for archivo in archivos_calificaciones:
        ruta_archivo = os.path.join(carpeta_calificaciones, archivo)
        filename = os.path.splitext(archivo)[0] + ".mp3"

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            respuesta = archivo.read()

        resultado = re.search(r'\d+', respuesta)

        if resultado:
            valor_satisfaccion = resultado.group(0)
            consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
            cursor.execute(consulta_existencia, (filename,))
            resultado_base = cursor.fetchone()

            if resultado_base[0] > 0:
                consulta = "UPDATE prueba_dana_calidad SET Reinsidencia = %s WHERE filename = %s"
                valores = (valor_satisfaccion, filename)
                cursor.execute(consulta, valores)
                print("La Reinsidencia del archivo {} ha sido actualizado en la base de datos.".format(filename))
            else:
                print("El archivo {} no existe en la base de datos. No se puede actualizar.".format(filename))
        else:
            print(f"No se encontró ninguna indicación de satisfacción del cliente en el archivo '{archivo}'.")

    conexion.commit()
    cursor.close()
    conexion.close()


def carga_de_base(guia,tipo):
    
    # ****************************** TABLA PRUEBA_DANA_CALIDAD
    import os
    import mysql.connector
    
    def guardar_transcripcion(filename, emociones):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET transcripcion = %s WHERE filename = %s"
            valores = (emociones, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, transcripcion) VALUES (%s, %s)"
            valores = (filename, emociones)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_transcripciones = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

        archivos_emociones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

        for archivo in archivos_emociones:
            ruta_archivo = os.path.join(carpeta_transcripciones, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                emociones = file.read()

            guardar_transcripcion(filename, emociones)



    #**************************************************************

    #BASE DE DATOS EMOCIONES
    import os
    import mysql.connector

    def guardar_emociones(filename, emociones):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()
        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            consulta = "UPDATE prueba_dana_calidad SET emociones = %s WHERE filename = %s"
            valores = (emociones, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            consulta = "INSERT INTO prueba_dana_calidad (filename, emociones) VALUES (%s, %s)"
            valores = (filename, emociones)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":

        carpeta_emociones = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\emociones'

        archivos_emociones = [f for f in os.listdir(carpeta_emociones) if f.endswith('.txt')]

        for archivo in archivos_emociones:
            ruta_archivo = os.path.join(carpeta_emociones, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r') as file:
                emociones = file.read()

            guardar_emociones(filename, emociones)

    #************************************ BASE DE DATOS CHAT
    import os
    import mysql.connector

    def guardar_chat(filename, chat):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET chat = %s WHERE filename = %s"
            valores = (chat, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, chat) VALUES (%s, %s)"
            valores = (filename, chat)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        
        carpeta_chat = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\chat'

        archivos_chat = [f for f in os.listdir(carpeta_chat) if f.endswith('.txt')]

        for archivo in archivos_chat:
            ruta_archivo = os.path.join(carpeta_chat, archivo)
            
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                chat = file.read()

            guardar_chat(filename, chat)
            
    #************************************ BASE TRANSCRIPCION ORIGINAL
    import os
    import mysql.connector

    def guardar_trans(filename, tra):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET transcripcion_original = %s WHERE filename = %s"
            valores = (tra, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, transcripcion_original) VALUES (%s, %s)"
            valores = (filename, tra)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_tra = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

        archivos_tra = [f for f in os.listdir(carpeta_tra) if f.endswith('.txt')]

        for archivo in archivos_tra:
            ruta_archivo = os.path.join(carpeta_tra, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                tra = file.read()

            guardar_trans(filename, tra)
    
    # ************************************ BASE EMOCIONES POR SEPARADO
    
    def guardar_resumen():
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        carpeta_local = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\emociones"

        try:
            
            cursor = conexion.cursor()

            for archivo in os.listdir(carpeta_local):
                if archivo.endswith(".txt"):
                    ruta_archivo = os.path.join(carpeta_local, archivo)

                    with open(ruta_archivo, "r") as file:
                        contenido = file.read()

                    nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"
                    negatividad = float(contenido.split("Puntuación de negatividad: ")[1].split("\n")[0])
                    neutralidad = float(contenido.split("Puntuación de neutralidad: ")[1].split("\n")[0])
                    positividad = float(contenido.split("Puntuación de positividad: ")[1].split("\n")[0])
                    puntuacion_total = float(contenido.split("Puntuación de sentimiento general: ")[1].split("\n")[0])

                    consulta = "UPDATE prueba_dana_calidad SET Negatividad = %s, Neutralidad = %s, Positividad = %s, Puntuacion_general_sentimientos = %s WHERE filename = %s"
                    valores = (negatividad, neutralidad, positividad, puntuacion_total, f"{nombre_archivo}")

                    cursor.execute(consulta, valores)

                    conexion.commit()

        except mysql.connector.Error as error:
            print(f"Error: {error}")

        finally:

            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
                print("Conexión cerrada.")


    if __name__ == "__main__":
        guardar_resumen()
        
    
    # ************************************BASE JUSIFICACION DE EMOCIONES
    
    import os
    import mysql.connector

    def guardar_trans(filename, justificacion):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM prueba_dana_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE prueba_dana_calidad SET justificacion_emociones = %s WHERE filename = %s"
            valores = (justificacion, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO prueba_dana_calidad (filename, justificacion_emociones) VALUES (%s, %s)"
            valores = (filename, justificacion)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_jus = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones'

        archivos_jus = [f for f in os.listdir(carpeta_jus) if f.endswith('.txt')]

        for archivo in archivos_jus:
            ruta_archivo = os.path.join(carpeta_jus, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                jus = file.read()

            guardar_trans(filename, jus)



    # ************************************ TABLA CONTEXTOS_CALIDAD

    #************************************* BASE DE DATOS PARA SUBIR RESUMEN
    import os
    import os.path
    import mysql.connector

    def guardar_resumen():
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        ruta_resumen = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\contextos_calidad'

        archivos_resumen = os.listdir(ruta_resumen)

        cursor.execute("SELECT filename FROM contextos_calidad")
        nombres_archivo_existente = [registro[0] for registro in cursor.fetchall()]

        for archivo in archivos_resumen:
            ruta_archivo = os.path.join(ruta_resumen, archivo)  

            nombre_archivo = os.path.splitext(archivo)[0] + ".mp3"
            
            consulta_existente = "SELECT filename FROM contextos_calidad WHERE filename = %s"
            cursor.execute(consulta_existente, (nombre_archivo,))
            resultado = cursor.fetchone()

            if nombre_archivo in nombres_archivo_existente:
                print(f"El archivo {nombre_archivo} ya fue subido. Saltando...")
                continue

            with open(ruta_archivo, "r", encoding='utf-8') as archivo_txt:
                linea = archivo_txt.read().strip()

            consulta = "INSERT INTO contextos_calidad (filename, contexto_general) VALUES (%s, %s)"
            valores = (nombre_archivo, linea)
            cursor.execute(consulta, valores)

        conexion.commit()

        cursor.close()
        conexion.close()


    if __name__ == "__main__":
        guardar_resumen()
    
    
    # ************************************BASE CONTEXTOS_CALIDAD RESUMEN
    
    import os
    import mysql.connector

    def guardar_trans(filename, resumen):
        conexion = mysql.connector.connect(
            host = "192.168.51.210",
            user = "root",
            password = "thor",
            database = "audios_dana"
        )

        cursor = conexion.cursor()

        
        consulta_existencia = "SELECT COUNT(*) FROM contextos_calidad WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            
            consulta = "UPDATE contextos_calidad SET resumen = %s WHERE filename = %s"
            valores = (resumen, filename)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
        else:
            
            consulta = "INSERT INTO contextos_calidad (filename, resumen) VALUES (%s, %s)"
            valores = (filename, resumen)
            cursor.execute(consulta, valores)
            print("El archivo {} ha sido agregado a la base de datos.".format(filename))

        conexion.commit()
        cursor.close()
        conexion.close()


    if __name__ == "__main__":
    
        carpeta_resumen = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\resumen'

        archivos_resumen = [f for f in os.listdir(carpeta_resumen) if f.endswith('.txt')]

        for archivo in archivos_resumen:
            ruta_archivo = os.path.join(carpeta_resumen, archivo)

            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                jus = file.read()

            guardar_trans(filename, jus)


    
            
    # *********************** BASE DE DATOS SOLUCION calificaciones************************

    import os
    import re
    import mysql.connector

    def actualizar_punto_de_vista(filename, punto_de_vista, guia):
        print("Subiendo punto de vista")
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )

        cursor = conexion.cursor()

        consulta_existencia = f"SELECT COUNT(*) FROM calificaciones_{guia} WHERE filename = %s"
        cursor.execute(consulta_existencia, (filename,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            consulta = f"UPDATE calificaciones_{guia} SET punto_de_vista = %s, Manejo_de_Herramientas = 15 WHERE filename = %s"
            valores = (punto_de_vista, filename)
            cursor.execute(consulta, valores)
            print(f"El punto de vista del archivo {filename} ha sido actualizado en la base de datos calificaciones_{guia}")
        else:
            print(f"El archivo {filename} no existe en la base de datos. No se puede actualizar.")

        conexion.commit()
        cursor.close()
        conexion.close()

    if __name__ == "__main__":

        carpeta_pov = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1'
        archivos_pov = [f for f in os.listdir(carpeta_pov) if f.endswith('.txt')]

        for archivo in archivos_pov:
            ruta_archivo_pov = os.path.join(carpeta_pov, archivo)
            filename = os.path.splitext(archivo)[0] + ".mp3"

            with open(ruta_archivo_pov, 'r', encoding='utf-8', errors='ignore') as file:
                punto_de_vista = file.read()

            # Insertar espacio antes de "Resumen" si está pegado a otra palabra
            punto_de_vista_limpio = re.sub(r'(?i)(\S)(Reclasificaci[oó]n)', r'\1 \2', punto_de_vista)

            # Eliminar contenido desde "Reclasificacion" en adelante
            punto_de_vista_limpio = re.sub(r'(?i)\s+Reclasificaci[oó]n[:\s]*\n?.*$', '', punto_de_vista_limpio, flags=re.DOTALL)


            actualizar_punto_de_vista(filename, punto_de_vista_limpio, guia)

    
    
    
    # CARGA DE SPEECH ANALYTICS
    # ****************************** TABLA PRUEBA_DANA_CALIDAD
    # import os
    # import mysql.connector
    
    # def guardar_speech_analytics(filename, emociones):
    #     conexion = mysql.connector.connect(
    #         host = "192.168.51.210",
    #         user = "root",
    #         password = "thor",
    #         database = "audios_dana"
    #     )

    #     cursor = conexion.cursor()

        
    #     consulta_existencia = "SELECT COUNT(*) FROM speech_analytics WHERE filename = %s"
    #     cursor.execute(consulta_existencia, (filename,))
    #     resultado = cursor.fetchone()

    #     if resultado[0] > 0:
            
    #         consulta = "UPDATE speech_analytics SET speech_analytic = %s WHERE filename = %s"
    #         valores = (emociones, filename)
    #         cursor.execute(consulta, valores)
    #         print("El archivo {} ha sido actualizado en la base de datos.".format(filename))
    #     else:
            
    #         consulta = "INSERT INTO speech_analytics (filename, speech_analytic) VALUES (%s, %s)"
    #         valores = (filename, emociones)
    #         cursor.execute(consulta, valores)
    #         print("El archivo {} ha sido agregado a la base de datos.".format(filename))

    #     conexion.commit()
    #     cursor.close()
    #     conexion.close()


    # if __name__ == "__main__":
    
    #     carpeta_transcripciones = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\speech_analytics'

    #     archivos_emociones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

    #     for archivo in archivos_emociones:
    #         ruta_archivo = os.path.join(carpeta_transcripciones, archivo)

    #         filename = os.path.splitext(archivo)[0] + ".mp3"

    #         with open(ruta_archivo, 'r', encoding='utf-8') as file:
    #             emociones = file.read()

    #         guardar_speech_analytics(filename, emociones)

    
    
    #reincidencia e insatisfaccion
    cliente_insatisfecho_cargar()
    reincidencia_cargar()
    cargar_motivo_problematica_sentimientos_solucion(guia,tipo)


            


if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        if guia == 'guia_set_1':
            tipo='servicios'
        elif guia == 'guia_set_9':
            tipo='soporte'
        elif guia == 'guia_set_10':
            tipo='soporte'
        elif guia == 'guia_set_11':
            tipo='soporte'
        elif guia == 'guia_set_12':
            tipo='retenciones'

        carga_de_base(guia,tipo)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " CARGA DE BASE DE DATOS MASIVA FINALIZADA CON EXITO ", "═"*30)
    
    # # MANUAL
    # guia = 'guia_set_9'
    # tipo='soporte'
    # carga_de_base(guia,tipo)