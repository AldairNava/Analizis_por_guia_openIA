import os
import mysql.connector
import openai
import json
import time
import sys
import traceback
import time
import re
from Tele import send_msg
from decouple import config

# FUNCIONES PARA USO DE CALIFICACIONES DIRECTAS CON ASISTENTE

# ASISTENTE SERVICIOS ---------------------------------------------------------------------------------------------------
# En la función hacer_pregunta_assiis_servicios:
def hacer_pregunta_assiis_servicios(pregunta, nombre_archivo):

    print("insertando llave")
    openai.api_key = config('OPENAI_API_KEY')
    print("insertando Id de asistente")
    assistant_id = config('assistant_id_servicios')
    thread = openai.beta.threads.create()
    
    def get_assistant_response(user_input):
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        start_time = time.time()

        while run.status != "completed":
            if time.time() - start_time > 90:
                raise TimeoutError("La solicitud ha tardado más de 90 segundos.")
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    try:
        print("preguntando Al asistente")
        user_input = pregunta
        response = get_assistant_response(user_input)
        print("analizis exitoso")
        return response
    except TimeoutError as e:
        print(f"Error tiempo de espera Excedido: {e}")
        # send_msg(f"Error Analizis masivo Mariana, tiempo de Respuesta excedido: {e}")

        # Actualizar estado en la base de datos por nombre de archivo
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )
        cursor = conexion.cursor()
        consulta_actualizacion = "UPDATE audios SET status = 'Reprocesar' WHERE audio_name = %s"
        cursor.execute(consulta_actualizacion, (nombre_archivo,))
        conexion.commit()
        cursor.close()
        conexion.close()

    except Exception as e:
        print(f"Error inesperado en el asistente: {e}")
        send_msg(f"Error Analizis masivo Mariana, Excepcion durante la consulta del asistente Servicios: {e}")

    
    

# ASISTENTE SOPORTE ---------------------------------------------------------------------------------------------------

def hacer_pregunta_assiis_soporte(pregunta, nombre_archivo):
    
    print("insertando llave")
    openai.api_key = config('OPENAI_API_KEY')
    print("insertando Id de asistente")
    assistant_id = config('assistant_id_soporte')
    thread = openai.beta.threads.create()

    def get_assistant_response(user_input):
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        start_time = time.time()

        while run.status != "completed":
            if time.time() - start_time > 90:
                raise TimeoutError("La solicitud ha tardado más de 90 segundos.")
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    try:
        print("preguntando Al asistente")
        user_input = pregunta
        response = get_assistant_response(user_input)
        print("analizis exitoso")
        return response
    except TimeoutError as e:
        print(f"Error tiempo de espera Excedido: {e}")
        # send_msg(f"Error Analizis masivo Mariana, tiempo de Respuesta excedido: {e}")

        # Actualizar estado en la base de datos por nombre de archivo
        conexion = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana"
        )
        cursor = conexion.cursor()
        consulta_actualizacion = "UPDATE audios SET status = 'Reprocesar' WHERE audio_name = %s"
        cursor.execute(consulta_actualizacion, (nombre_archivo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"Error inesperado en el asistente: {e}")
        send_msg(f"Error Analizis masivo Mariana, Excepcion durante la consulta del asistente Soporte: {e}")


# ASISTENTE RETENCIONES ---------------------------------------------------------------------------------------------------
def hacer_pregunta_assiis_retenciones(pregunta, nombre_archivo):
    
    print("insertando llave")
    openai.api_key = config('OPENAI_API_KEY')
    print("insertando Id de asistente")
    assistant_id = config('assistant_id_retencion')
    thread = openai.beta.threads.create()

    def get_assistant_response(user_input):
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        start_time = time.time()  # Registrar el tiempo de inicio

        while run.status != "completed":
            if time.time() - start_time > 90:  # Si han pasado más de 90 segundos
                print("la solicitud tardó más de 90 segundos")
                return None  # Romper el bucle y retornar None
                
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    try:
        print("preguntando al asistente")
        user_input = pregunta
        response = get_assistant_response(user_input)
        if response is not None:
            print("análisis exitoso")
            return response
        else:
            print("No se recibió una respuesta en el tiempo esperado.")
            # Actualizar estado en la base de datos por nombre de archivo
            conexion = mysql.connector.connect(
                host="192.168.51.210",
                user="root",
                password="thor",
                database="audios_dana"
            )
            cursor = conexion.cursor()
            consulta_actualizacion = "UPDATE audios SET status = 'Reprocesar' WHERE audio_name = %s"
            cursor.execute(consulta_actualizacion, (nombre_archivo,))
            conexion.commit()
            cursor.close()
            conexion.close()
            return None
            
    except Exception as e:
        print(f"Error inesperado en el asistente: {e}")
        send_msg(f"Error análisis masivo Mariana, Excepción durante la consulta del asistente Soporte: {e}")
        return None









# FUNCIONES PARA USO DE CALIFICACIONES DIRECTAS CON GPT

def hacer_pregunta_min_tokens(fragmento_texto):
    openai.api_key = config('OPENAI_API_KEY')
    completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
                {"role": "system", "content": "Analista de calidad con 30 años de experiencia en call center para servicios de televisión, internet y telefonía."},
                {"role": "user", "content": fragmento_texto}
    ]
    )
    respuesta = completion.choices[0].message.content
    return respuesta






# ****************** obenter calificaciones del audio (json y tabla)
def guia_set(guia, carpeta_archivos, carpeta_data):
    print("\n--------- INICIANDO PROCESO DE CALIFICACIÓN POR GUIA ---------\n")
    start_time = time.time()

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    try:
        cursor = conexion.cursor()

        consulta = f"SELECT nombre_punto, contexto FROM {guia} WHERE nombre_punto <> 'Manejo_de_Herramientas';"
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        for archivo in os.listdir(carpeta_archivos):
            if archivo.endswith(('.txt', '.doc', '.docx')):
                local_txt_path = os.path.join(carpeta_data, 'pov', f"{os.path.splitext(archivo)[0]}.txt")

                with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
                    for resultado in resultados:
                        archivo_txt.write(f"'{resultado[0]}': {resultado[1]}\n")

                    print(f"\nDatos guardados de {guia} en {local_txt_path}\n")

                ruta_archivo = os.path.join(carpeta_archivos, archivo)
                ruta_resultado_json = os.path.join(carpeta_data, 'pov1', f"{os.path.splitext(archivo)[0]}.txt")

                with open(ruta_archivo, 'r', encoding='utf-8') as archivo_lectura:
                    texto_completo = archivo_lectura.read()
                    
                pregunta2 = f''' Analiza el siguiente texto: {texto_completo} dame lo siguiente:
                                    - Reclasificacion: : clasiifca el tipo de llamada, solo clasifica entre estos 3 tipos de llamada (Servicios,Soporte,Retencion):
                                                        Servicios cualquiera de los siguientes puntos expresados por el cliente:
                                                        -Aclaraciones
                                                        -Cargos no Reconocidos
                                                        -Reembolsos
                                                        -Pagos (incluye expresiones como “ya pagué”)
                                                        -Consulta de saldo
                                                        -Ajustes
                                                        -Facturación
                                                        -Cambios
                                                        -Quejas
                                                        Nota: Agrupa términos o expresiones con significados similares.

                                                        Soporte Internet: Fallas relacionadas con el servicio de internet.
                                                        Soporte Video: Fallas relacionadas con el servicio de televisión, incluyendo problemas en apps de streaming.
                                                        Soporte Telefonía: Fallas relacionadas con el servicio telefónico.
                                                        Importante: Excluye de esta categoría los casos en que la falla en el servicio se deba a falta de pago, suspensión por impago u otros motivos relacionados con la facturación. Si se detecta que la causa de la falla es la falta de pago, la llamada debe ser clasificada como Servicios.

                                                        Retención:
                                                        Se refiere a cualquier intento de cancelación del servicio por parte del cliente o a estrategias de retención/renovación ofrecidas por el agente.
                                    - ResumenFront: Resumen breve de la transcripcion
                                    - problematica: 
                                    - eficiencia del agente: % 
                                    - el tipo de llamada:
                                    - frases mas repetidas:
                                    - Confirmacion de titular: Si / No es el titular.
                                    - Motivo de la llamada: Clasificacion corta sobre las razones expresadas por el cliente en su llamada.
                                    - Solucion: Solucionado o No solucionado.
                                    - Sentimientos: Frustración, Enojo, Satisfacción, Duda ocualquier otra emocion expresada.
                                    - Tendencias: Identifica las tendencias en esta transcripcion.
                                    - Datos de Actualizacion: Verifica que el agente ofrecio actualizacion de datos CURP y whatsApp. Dime que datos se actualizaron , de lo contario (No se ofrecio actualizacion de datos)
                                    - Resultado de la llamada: Clasificacion corta sobre el resultado de la llamada.
                                    - Reincidencia: Valor 1 si es problema reportado varias veces por el cliente , si no 0.
                                    - Insatisfacción: 1 si el cliente termina insastifecho , si no 0.
                                    - Explicación emocional: explicacion emocional breve y detallada.
                                    - Llamada cortada: explica el por que de la llamada cortada
                                    IMPORTANTE: Evita colocar "-", ".-", "*", "#" o viñetas similares en la lista, SOLO SEPARALOS POR SALTOS DE LINEA Y MAYUSCULAS COLOCANDO LAS RESPUESTAS SOBRE LA MISMA LINEA
                                    '''
                try:
                    print("haciendo pregunta 1")
                    respuesta2 = hacer_pregunta_min_tokens(pregunta2)
                    print (respuesta2)
                except Exception as e :
                    print(f"Error{e}")

                clasificacion = re.search(r'(?i)Reclasificaci[oó]n[:\s]*\n?(.+)', respuesta2)

                if clasificacion:
                    tipo_llamada = clasificacion.group(1).strip()
                    if tipo_llamada.lower() in ['retencion', 'retención', 'cancelación']:
                        guia = "guia_set_12"
                    elif tipo_llamada.lower() in ['servicios','soporte servicios','servicio']:
                        guia = "guia_set_1"
                    elif tipo_llamada.lower() in ['soporte telefonia','telefonia','Telefonía','soporte telefonía']:
                        guia = "guia_set_10"
                    elif tipo_llamada.lower() in ['soporte internet','Internet','internet']:
                        guia = "guia_set_9"
                    elif tipo_llamada.lower() in ['soporte video','Video','video']:
                        guia = "guia_set_11"
                    else:
                        print (f"la guia no se pudo asignar")
                    print(f"Tipo de Llamada: {tipo_llamada}, Guía: {guia}")
                else:
                    print("No se encontró el tipo de llamada en la respuesta.")
                
                print(guia)

                # time.sleep(1000)            
                   
                
                #PROCESO DE FORMULACION DE PREGUNTAS
                   
                if guia == 'guia_set_1':
                    pregunta_servicios = f"""
                                    califica la transcripción proporcionada con el siguiente formato, ten en cuenta que es un ejemplo, debe de calificar con los parámetros del archivo adjunto:

                                    Tengo la siguiente transcripción de una llamada telefónica: , Como EXPERTO EN CALL CENTER de telecomunicaciones EN EL AREA de calidad con mas de 25 años de experiencia, evalúa si el agente cumple lo siguientes Criterios, toma en cuenta sinónimos y los ejemplos que se describen, asigna en valor de 1 si cumple el parámetro y el valor de 0 si no cumple el parámetro: 

                                    Si no aplica O NO SE MENCIONA, NO LO ETIQUETES COMO 'N/A' o 0; asigne el valor de 1 SIEMPRE

                                    **INSTRUCCIÓN IMPORTANTE: Muestra los resultados en formato de json (parametro, calificaciones), sigue forzosamente este formato
                                    ejemplo:

                                    json


                                        parametro: 1 o 0 dependiendo si cumple o no el parámetro


                                                            

                                    **INSTRUCCIÓN IMPORTANTE:  Además muestra los resultados en formato de tabla (parametro, calificaciones, justificacion_PROMPT y descripcion_penalizacion)
                                    **INSTRUCCIÓN IMPORTANTE:  1.- En el apartado de la "justificacion_PROMPT", si y solo si existe una penalización, es decir un 0 en Calificacion, solo puede colocarse la penalización , utiliza  la lista "2.- LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto.
                                    **INSTRUCCIÓN IMPORTANTE:  2.- En el apartado de "descripcion_penalizacion", si y solo si existe una penalización, es decir un 0  en Calificacion, se colocara una justificación detallada de porque no cumplió el parámetro.
                                    **INSTRUCCIÓN IMPORTANTE:  3.- En la fila de "groserias", si y solo si existe una falla critica, es decir un 0 en Calificacion, solo puede colocarse la FALLA CRITICA ENCONTRADA EN EL TEXTO del parámetro de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.

                                    **INSTRUCCIÓN IMPORTANTE: 4.- En caso de que cumpla el parámetro, es decir que en Calificación tenga un 1, no será necesario colocar ninguno de los puntos 1 y 2.
                                    ejemplo:

                                    |    Parametro        |  Calificacion   |   justificacion_PROMPT      |     descripcion_penalizacion          |                                                     
                                    |nombre del parámetro |     0           |   justificación del PROMPT  |   justificación detallada de la penalización por la IA  |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     0           |   justificación del PROMPT  | justificación detallada de la penalización por la IA   |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |groserias            |     0           |                             | justificación de la falla critica con respecto de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.  |

                                    **INSTRUCCIÓN IMPORTANTE solo afecta a estos parametros:
                                    Script_entrada: Siempre pon 1.
                                    Validacion de datos: Si se encuentra una coincidencia de busqueda por nombre del titular o confirmacion de Titular ponle 1 si no 0.
                                    Preguntas_sin_responder: Siempre pon 1.
                                                            
                                    **INSTRUCCIÓN IMPORTANTE: - RESPETA LOS VALORES QUE VAN EN CADA COLUMNA, EN CALIFICACION SOLO VAN 1 O 0, EN justificacion_PROMPT Utiliza LA LISTA "LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto. CUANDO EL VALOR DE CALIFICACION ES 0 Y EN descripcion_penalizacion SOLO VA LA JUSTIFICACION DE LA PENALIZACION HECHA POR LA IA.

                                    **INSTRUCCIÓN IMPORTANTE:  NO OLVIDES PENALIZAR TILIZANDO LA LISTA DE PENALIZACIONES DEL ARCHIVO ADJUNTO "lista de penalizaciones y fallas criticas". 


                                    **INSTRUCCIÓN IMPORTANTE:  NO OLVIDES PENALIZAR LAS FALLAS CRITICAS UTILIZANDO LA LISTA DE FALLAS CRITICAS DEL ARCHIVO ADJUNTO "lista de penalizaciones y fallas criticas". 
                                                        
                                    -  Además dame puntos a mejorar durante la conversación CON LA FRASE 'Puntos a mejorar durante la conversación:' en forma de lista pero no los enumeres, solo con separación de espacios, NO AGREGES BIÑETAS NI NUMEROS, SOLO CON SEPARACION CON SALTOS DE LINEA, ejemplo:
                                    Evita colocar "-", ".-", "*", "#" o viñetas similares en la lista, SOLO SEPARALOS POR SALTOS DE LINEA
                                        
                                    transcripcion: {texto_completo}
                                        """
                
                elif guia == 'guia_set_12':
                    
                    pregunta_retencion = f"""
                                    califica la transcripción proporcionada con el siguiente formato, ten en cuenta que es un ejemplo, debe de calificar con los parámetros del archivo adjunto:

                                    Tengo la siguiente transcripción de una llamada telefónica: , Como EXPERTO EN CALL CENTER de telecomunicaciones EN EL AREA de calidad con mas de 25 años de experiencia, evalúa si el agente cumple lo siguientes Criterios, toma en cuenta sinónimos y los ejemplos que se describen, asigna en valor de 1 si cumple el parámetro y el valor de 0 si no cumple el parámetro: 

                                    Si no aplica O NO SE MENCIONA, NO LO ETIQUETES COMO 'N/A' o 0; asigne el valor de 1 SIEMPRE

                                    **INSTRUCCIÓN IMPORTANTE: Muestra los resultados en formato de json (parametro, calificaciones), sigue forzosamente este formato
                                    ejemplo:

                                    json


                                        parametro: 1 o 0 dependiendo si cumple o no el parámetro



                                    **INSTRUCCIÓN IMPORTANTE:  Además muestra los resultados en formato de tabla (parametro, calificaciones, justificacion_PROMPT y descripcion_penalizacion)
                                    **INSTRUCCIÓN IMPORTANTE:  1.- En el apartado de la "justificacion_PROMPT", si y solo si existe una penalización, es decir un 0 en Calificacion, solo puede colocarse la penalización , utiliza  la lista "2.- LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto.
                                    **INSTRUCCIÓN IMPORTANTE:  2.- En el apartado de "descripcion_penalizacion", si y solo si existe una penalización, es decir un 0  en Calificacion, se colocara una justificación detallada de porque no cumplió el parámetro.
                                    **INSTRUCCIÓN IMPORTANTE:  3.- En la fila de "groserias", si y solo si existe una falla critica, es decir un 0 en Calificacion, solo puede colocarse la FALLA CRITICA ENCONTRADA EN EL TEXTO del parámetro de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.

                                    **INSTRUCCIÓN IMPORTANTE: 4.- En caso de que cumpla el parámetro, es decir que en Calificación tenga un 1, no será necesario colocar ninguno de los puntos 1 y 2.
                                    ejemplo:

                                    |    Parametro        |  Calificacion   |   justificacion_PROMPT      |     descripcion_penalizacion          |                                                     
                                    |nombre del parámetro |     0           |   justificación del PROMPT  |   justificación detallada de la penalización por la IA  |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     0           |   justificación del PROMPT  | justificación detallada de la penalización por la IA   |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |groserias            |     0           |                             | justificación de la falla critica con respecto de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.  |
                                                            
                                    **INSTRUCCIÓN IMPORTANTE: - RESPETA LOS VALORES QUE VAN EN CADA COLUMNA, EN CALIFICACION SOLO VAN 1 O 0, EN justificacion_PROMPT Utiliza LA LISTA "LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto. CUANDO EL VALOR DE CALIFICACION ES 0 Y EN descripcion_penalizacion SOLO VA LA JUSTIFICACION DE LA PENALIZACION HECHA POR LA IA.

                                    **INSTRUCCIÓN IMPORTANTE:  NO OLVIDES PENALIZAR TILIZANDO LA LISTA DE PENALIZACIONES DEL ARCHIVO ADJUNTO "lista de penalizaciones y fallas criticas". 


                                    **INSTRUCCIÓN IMPORTANTE:  NO OLVIDES PENALIZAR LAS FALLAS CRITICAS UTILIZANDO LA LISTA DE FALLAS CRITICAS DEL ARCHIVO ADJUNTO "lista de penalizaciones y fallas criticas". 
                                                        
                                    -  Además dame puntos a mejorar durante la conversación CON LA FRASE 'Puntos a mejorar durante la conversación:' en forma de lista pero no los enumeres, solo con separación de espacios, NO AGREGES BIÑETAS NI NUMEROS, SOLO CON SEPARACION CON SALTOS DE LINEA, ejemplo:
                                    Evita colocar "-", ".-", "*", "#" o viñetas similares en la lista, SOLO SEPARALOS POR SALTOS DE LINEA
                                    
                                    **INSTRUCCIÓN IMPORTANTE solo afecta a estos parametros:
                                    Script_entrada: Siempre pon 1.
                                    Validacion de datos: Si se encuentra una coincidencia de busqueda por cuenta , telefono o nombre del titular ponle 1 si no 0.
                                    Preguntas_sin_responder: Siempre pon 1.
                                        
                                    transcripcion: {texto_completo}
                                        """
                
                
                elif guia == 'guia_set_9' or guia == 'guia_set_10' or guia == 'guia_set_11':
                    # PREGUNTA A ASISTENTE PARA SOPORTE
                    pregunta_soporte = f"""
                                    califica la transcripción proporcionada con el siguiente formato, ten en cuenta que es un ejemplo, debe de calificar con los parámetros del archivo adjunto:

                                    Tengo la siguiente transcripción de una llamada telefónica: {texto_completo} , Como EXPERTO EN CALL CENTER de telecomunicaciones EN EL AREA de calidad con mas de 25 años de experiencia, evalúa si el agente cumple lo siguientes Criterios, toma en cuenta sinónimos y los ejemplos que se describen, asigna en valor de 1 si cumple el parámetro y el valor de 0 si no cumple el parámetro: 

                                    Si no aplica O NO SE MENCIONA, NO LO ETIQUETES COMO 'N/A' o 0; asigne el valor de 1 SIEMPRE

                                    **INSTRUCCIÓN IMPORTANTE: Muestra los resultados en formato de json (parametro, calificaciones), sigue forzosamente este formato
                                    ejemplo:

                                    json


                                        parametro: 1 o 0 dependiendo si cumple o no el parámetro


                                                            

                                    **INSTRUCCIÓN IMPORTANTE:  Además muestra los resultados en formato de tabla (parametro, calificaciones, justificacion_PROMPT y descripcion_penalizacion)
                                    **INSTRUCCIÓN IMPORTANTE:  1.- En el apartado de la "justificacion_PROMPT", si y solo si existe una penalización, es decir un 0 en Calificacion, solo puede colocarse la penalización , utiliza  la lista "2.- LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto.
                                    **INSTRUCCIÓN IMPORTANTE:  2.- En el apartado de "descripcion_penalizacion", si y solo si existe una penalización, es decir un 0  en Calificacion, se colocara una justificación detallada de porque no cumplió el parámetro.
                                    **INSTRUCCIÓN IMPORTANTE:  3.- En la fila de "groserias", si y solo si existe una falla critica, es decir un 0 en Calificacion, solo puede colocarse la FALLA CRITICA ENCONTRADA EN EL TEXTO del parámetro de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.

                                    **INSTRUCCIÓN IMPORTANTE: 4.- En caso de que cumpla el parámetro, es decir que en Calificación tenga un 1, no será necesario colocar ninguno de los puntos 1 y 2.
                                    ejemplo:

                                    |    Parametro        |  Calificacion   |   justificacion_PROMPT      |     descripcion_penalizacion          |                                                     
                                    |nombre del parámetro |     0           |   justificación del PROMPT  |   justificación detallada de la penalización por la IA  |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     0           |   justificación del PROMPT  | justificación detallada de la penalización por la IA   |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |nombre del parámetro |     1           |                             |                                                                                                |
                                    |groserias            |     0           |                             | justificación de la falla critica con respecto de la lista "3.- LISTADO DE FALLAS CRITICAS" del archivo de entrenamiento.  |
                                                            
                                    **INSTRUCCIÓN IMPORTANTE: - RESPETA LOS VALORES QUE VAN EN CADA COLUMNA, EN CALIFICACION SOLO VAN 1 O 0, EN justificacion_PROMPT Utiliza LA LISTA "LISTA DE PENALIZACIONES" del archivo de entrenamiento adjunto. CUANDO EL VALOR DE CALIFICACION ES 0 Y EN descripcion_penalizacion SOLO VA LA JUSTIFICACION DE LA PENALIZACION HECHA POR LA IA.


                                    **INSTRUCCIÓN IMPORTANTE:  NO OLVIDES PENALIZAR LAS FALLAS CRITICAS UTILIZANDO LA LISTA DE FALLAS CRITICAS DEL ARCHIVO ADJUNTO "lista de penalizaciones y fallas criticas". 
                                                        
                                    -  Además dame puntos a mejorar durante la conversación CON LA FRASE 'Puntos a mejorar durante la conversación:' en forma de lista pero no los enumeres, solo con separación de espacios, NO AGREGES BIÑETAS NI NUMEROS, SOLO CON SEPARACION CON SALTOS DE LINEA, ejemplo:
                                    Evita colocar "-", ".-", "*", "#" o viñetas similares en la lista, SOLO SEPARALOS POR SALTOS DE LINEA
                                    
                                    **INSTRUCCIÓN IMPORTANTE solo afecta a estos parametros:
                                    Script_entrada: Siempre pon 1.
                                    Validacion de datos: Si se encuentra una coincidencia de busqueda por nombre del titular o confirmacion de Titular ponle 1 si no 0.
                                    Preguntas_sin_responder: Siempre pon 1.
                                        """
                # Proceso de consulta a asistentes
                try:
                    if guia == 'guia_set_1':
                        print("Accediendo asistente servicios")
                        respuesta = hacer_pregunta_assiis_servicios(pregunta_servicios, archivo)
                        
                    elif guia == 'guia_set_9' or guia == 'guia_set_10' or guia == 'guia_set_11':
                        print("Accediendo asistente soporte")
                        respuesta = hacer_pregunta_assiis_soporte(pregunta_soporte, archivo)
                        
                    elif guia == 'guia_set_12':
                        print("Accediendo asistente retenciones")
                        respuesta = hacer_pregunta_assiis_retenciones(pregunta_retencion, archivo)

                    if respuesta is not None:
                        print("\n", respuesta, "\n")
                        with open(ruta_resultado_json, 'a', encoding='utf-8') as archivo_txt:
                            archivo_txt.write(respuesta+ '\n\n')
                            

                        with open(ruta_resultado_json, 'a', encoding='utf-8') as archivo_txt:
                            archivo_txt.write(respuesta2 + '\n') 

                        print(f"\nPregunta dos guardada '{archivo}' guardada en '{ruta_resultado_json}'\n")
                    else:
                        print(f"No se obtuvo respuesta para el archivo {archivo}. Continuando con los demás.")
                        continue

                except Exception as e:
                    print(f"Error procesando el archivo {archivo}: {e}")
                    # Actualizar estado en la base de datos por nombre de archivo en caso de error
                    try:
                        cursor_actualizacion = conexion.cursor()
                        consulta_actualizacion = "UPDATE audios SET status = 'Reprocesar' WHERE audio_name = %s"
                        cursor_actualizacion.execute(consulta_actualizacion, (archivo,))
                        conexion.commit()
                        cursor_actualizacion.close()
                        print(f"Estado actualizado para el archivo {archivo}. Continuando con los demás.")
                    except mysql.connector.Error as db_error:
                        print(f"Error actualizando el estado del archivo {archivo}: {db_error}")
                    continue  # Continuar con el siguiente archivo
        extraccion(guia)
        extraccion_1()
        extraccion_2()
        eliminar_comillas_numeros_en_carpeta()
        comparacion()
        eliminar_json()
        cargar_calificaciones_en_mysql(guia)
        # time.sleep(1000)

    except mysql.connector.Error as error:
        print(f"\nError en la conexión a la base de datos: {error}\n")
        send_msg(f"Error en la conexión a la base de datos: {error}")

    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print("\nTiempo de ejecución: {:.2f} segundos".format(execution_time))






# *********************** crear json del prompt de la base de datos
def extraccion(guia):
    print("\nINICIANDO EXTRACCION DE CALIFICACIONES\n")
    start_time = time.time()

    carpeta_data = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion'

    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )

    try:
        cursor = conexion.cursor()

        consulta = f"SELECT nombre_punto, puntaje FROM {guia} WHERE nombre_punto <> 'Manejo_de_Herramientas';"
        cursor.execute(consulta)
        resultados = cursor.fetchall()


        local_txt_path = os.path.join(carpeta_data, 'pov2', "tabla_puntaje.txt")

        with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
            for resultado in resultados:
                archivo_txt.write(f"'{resultado[0]}': {resultado[1]}\n")

            print(f"\nDatos guardados de {guia} en {local_txt_path}\n")

        with open(local_txt_path, 'r', encoding='utf-8') as archivo_lectura:
            contenido_archivo = archivo_lectura.read()

        pregunta2 = f"""Tengo la siguiente informacion: {contenido_archivo}

                        Muestra los resultados en formato de json (parametro, calificaciones), no me des mas contexto mas que el json, SOLO QUIERO EL JSON y no modifiques mayusculas y minuculas
                        ejemplo

                        {{
                            "parametro: calificacion"
                        }}

                    """

        respuesta2 = hacer_pregunta_min_tokens(pregunta2)

        print("\n", respuesta2, "\n")

        local_txt_path = os.path.join(carpeta_data, 'pov3', "tabla_puntaje_json.txt")

        with open(local_txt_path, "w", encoding='utf-8') as archivo_txt:
            archivo_txt.write(respuesta2)

    except mysql.connector.Error as error:  
        print(f"\nError: {error}\n")

    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()
            
    end_time = time.time()
    execution_time = end_time - start_time
    print("\nTiempo de ejecución: {:.2f} segundos\n".format(execution_time))
    
    
    
    

#*********************** extraccion de json del archivo 1
def extraccion_1():
    
    print("\nINICIANDO EXTRACCION DE PRIMER JSON\n")

    carpeta_entrada = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1'

    carpeta_salida = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_1'

    for nombre_archivo in os.listdir(carpeta_entrada):

        ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)

        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio_json = texto_completo.find("{")

            json_str = texto_completo[inicio_json:]

            fin_json = json_str.rfind("}") + 1

            json_str = json_str[:fin_json]

            try:
                json_data = json.loads(json_str)

                ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo[:-4]}.json")

                with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
                    json.dump(json_data, archivo_salida, indent=2)

                print(f"\nResultado guardado en: {ruta_salida}\n")
            except json.decoder.JSONDecodeError as e:
                print(f"\nError al cargar el JSON en el archivo {nombre_archivo}: {e}\n")




#*********************** extraccion de json del archivo 2                
def extraccion_2():
    
    print("\nINICIANDO EXTRACCION DE SEGUNDO JSON\n")

    carpeta_entrada = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov3'
    carpeta_salida = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_2'

    for nombre_archivo in os.listdir(carpeta_entrada):

        ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)

        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio_json = texto_completo.find("{")

            json_str = texto_completo[inicio_json:]

            fin_json = json_str.rfind("}") + 1

            json_str = json_str[:fin_json]

            try:
                json_data = json.loads(json_str)

                ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo[:-4]}.json")

                with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
                    json.dump(json_data, archivo_salida, indent=2)

                print(f"\nResultado guardado en: {ruta_salida}\n")
            except json.decoder.JSONDecodeError as e:
                print(f"\nError al cargar el JSON en el archivo {nombre_archivo}: {e}\n")
                
                
                
                
#*********************** ELIMINA COMILLAS DOBLES
                
def eliminar_comillas_numeros_en_carpeta():
    ruta_carpeta = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_1'
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_json = os.path.join(ruta_carpeta, nombre_archivo)

        if nombre_archivo.endswith('.json') and os.path.isfile(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for key, value in data.items():
                if isinstance(value, str) and value.isdigit():
                    data[key] = int(value)

            with open(ruta_json, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
                
                
                
                

#*********************** COMPARACION DE LOS JSON
def comparacion():
    print("\nINICIANDO COMPARACION DE JSON pov4\n")

    folder_path_json1 = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_1'
    folder_path_json2 = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_2'
    output_folder = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov4'

    for filename in os.listdir(folder_path_json1):
        file_path_json1 = os.path.join(folder_path_json1, filename)
        file_path_json2 = os.path.join(folder_path_json2, "tabla_puntaje_json.json")

        try:
            with open(file_path_json1, 'r', encoding='utf-8') as file:
                json1_str = file.read()

            with open(file_path_json2, 'r', encoding='utf-8') as file:
                json2_str = file.read()

            json1 = json.loads(json1_str)
            json2 = json.loads(json2_str)

            for key, value in json1.items():
                if value == 1 or value == "1":
                    json1[key] = json2.get(key, value)

            suma_anterior = sum(
                json1[key] for key in json1 
                if key not in ["groserias", "resultado", "Manejo_de_Herramientas"] and isinstance(json1[key], (int, float))
            )

            if "groserias" in json2:
                json1["resultado"] = suma_anterior

            output_file_path = os.path.join(output_folder, f"{filename}")

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(json1, output_file, indent=2)

            print(f"\nResultado para el archivo {filename} guardado en {output_file_path}\n")

        except FileNotFoundError as e:
            print(f"\nError: El archivo {filename} no se encuentra en ambas carpetas.\n")
        except json.JSONDecodeError as e:
            print(f"\nError al decodificar el JSON en el archivo {filename}: {e}\n")


            
            



#*********************** ELIMINA FORMATO JSON Y DEJA SOLO TABLA DE CALIFICACIONES

def eliminar_json():
    archivo_a_analizar = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1"

    carpeta_salida = r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\contextos_calidad"
    
    for nombre_archivo in os.listdir(archivo_a_analizar):
        ruta_entrada = os.path.join(archivo_a_analizar, nombre_archivo)
        if os.path.isfile(ruta_entrada) and nombre_archivo.endswith('.txt'):

            with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
                texto_completo = archivo.read()

            inicio = texto_completo.find('{')
            fin = texto_completo.rfind('}')

            if inicio != -1 and fin != -1:
                texto_completo = texto_completo[:inicio] + texto_completo[fin + 1:]
                
            inicio1 = texto_completo.find('```json')
            fin1 = texto_completo.rfind('```')

            if inicio1 != -1 and fin1 != -1:
                texto_completo = texto_completo[:inicio1] + texto_completo[fin1 + 1:]

            try:
                # Corregir la línea siguiente
                output_file = os.path.join(carpeta_salida, os.path.basename(ruta_entrada))
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(texto_completo)

                print(f"Se ha eliminado el texto entre las llaves y el resultado se ha guardado en: {output_file}")
            
            except traceback as e:
                print(f"\nError al obtener el archivo: {e}\n")



            
#*********************** CARGA DE CALIFICACIONES A LA BASE DE DATOS


def archivo_ya_subido(cursor, guia, filename):
    cursor.execute(f"SELECT 1 FROM calificaciones_{guia} WHERE filename = %s", (filename,))
    return cursor.fetchone() is not None

def cargar_calificaciones_en_mysql(guia):
    print(f"\nINICIO DE SUBIDA DE BASE DE DATOS {guia}\n")

    conn = mysql.connector.connect(
        host='192.168.51.210',
        user='root',
        password='thor',
        database='audios_dana'
    )

    cursor = conn.cursor()

    json_folder = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov4'

    for filename in os.listdir(json_folder):
        file_path = os.path.join(json_folder, filename)

        try:
            with open(file_path, 'r') as file:
                json_str = file.read()

            json_data = json.loads(json_str)

            file_name_without_extension, _ = os.path.splitext(filename)

            json_data['filename'] = file_name_without_extension + '.mp3'
            
            if archivo_ya_subido(cursor, guia, json_data['filename']):
                print(f"\nEl archivo {filename} ya ha sido subido a la tabla {guia}. Actualizando valores...\n")

                cursor.execute(f"SHOW COLUMNS FROM calificaciones_{guia}")
                column_names = [column[0] for column in cursor.fetchall()]

                # Excluir 'id_audio' de las columnas
                column_names = [column for column in column_names if column != 'id_audio']

                update_fields = ', '.join([f"{column} = %s" for column in column_names])
                sql_query = f'''
                    UPDATE calificaciones_{guia} SET {update_fields}
                    WHERE filename = %s
                '''

                values = [json_data.get(column, None) for column in column_names]
                values.append(json_data['filename'])

                cursor.execute(sql_query, values)
                conn.commit()

                print(f"\nValores de {filename} actualizados en la base de datos calificaciones_{guia}.\n")

            else:
                cursor.execute(f"SHOW COLUMNS FROM calificaciones_{guia}")
                column_names = [column[0] for column in cursor.fetchall()]

                sql_query = f'''
                    INSERT INTO calificaciones_{guia} ({', '.join(column_names)})
                    VALUES ({', '.join(['%s']*len(column_names))})
                '''
                
                values = [json_data.get(column, None) for column in column_names]

                cursor.execute(sql_query, values)

                conn.commit()

                print(f"\nValores de {filename} insertados en la base de datos calificaciones_{guia}.\n")

            tipo = None
            if guia == "guia_set_1":
                tipo = "servicios"
            elif guia in ["guia_set_9", "guia_set_10", "guia_set_11"]:
                tipo = "soporte"
            elif guia == "guia_set_12":
                tipo = "retenciones"

            cursor.execute("UPDATE audios SET guia = %s, tipo = %s WHERE audio_name = %s", (guia, tipo, json_data['filename']))
            conn.commit()
            
            print(f"\nArchivo {json_data['filename']} actualizado: guia = {guia}, tipo = {tipo}\n")

        except FileNotFoundError as e:
            print(f"\nError: El archivo {filename} no se encuentra en la carpeta.\n")
        except json.JSONDecodeError as e:
            print(f"\nError al decodificar el JSON en el archivo {filename}: {e}\n")
        except mysql.connector.Error as e:
            print(f"\nError de MySQL: {e}\n")
        except KeyError as e:
            print(f"\nError: {e}\n")

    cursor.close()
    conn.close()

    print("proceso finalizado")



def main():
    start_time = time.time()
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        carpeta_archivos = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'
        carpeta_data = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion'
        guia_set(guia, carpeta_archivos, carpeta_data)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " Calificacion terminada con exito ", "═"*30)
    end_time = time.time()
    execution_time = end_time - start_time 
    print("\nTiempo de ejecución: {:.2f} segundos\n".format(execution_time))

    

if __name__ == "__main__":
    main()
    