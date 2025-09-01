import subprocess
import requests
import mysql.connector
import time
import re
import datetime
import os
from Tele import send_msg

def consultar_Transcritos():
    """Consulta la base de datos para verificar registros con status 'Transcrito'."""
    conexion = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="thor",
        database="audios_dana"
    )
    cursor = conexion.cursor()
    consulta = "SELECT count(*) FROM audios WHERE status in ('Transcrito')"
    cursor.execute(consulta)
    resultado = cursor.fetchone()[0]
    conexion.close()
    
    return resultado

def ejecutar_script(script):
    resultado = subprocess.run(["python", script], capture_output=True, text=True)
    return resultado.returncode

def flujo_Principal():
    send_msg("Analizis Masivo Iniciado")
    print("\nLimpiando las carpetas para Iniciar la carga\n")
    subprocess.run(["python", "eliminar_datos.py"])
    
    while True:
        print("\nEXTRAYENDO DATOS DE SERVICIO DE LA Base")
        resultado_servicio = ejecutar_script("extraccion_datos_base_servicios.py")
        
        if resultado_servicio == 0:
            print("audios Extraidos..")
            guia = 'guia_set_1'
            tipo = 'servicios'
            print(guia)
            print(tipo)
        else:
            print("Servicios vacias procedeiendo con SOPORTE VIDEO")
            print("\nEXTRAYENDO DATOS DE SOPORTE VIDEO DE LA BASE")
            resultado_soporte_video = ejecutar_script("extraccion_datos_base_soporte_video.py")
            
            if resultado_soporte_video == 0:
                print("audios Extraidos..")
                guia = 'guia_set_11'
                tipo = 'soporte'
                print(guia)
                print(tipo)
            else:
                print("Soporte video vacia procedeiendo con Soporte Internet")
                print("\nEXTRAYENDO DATOS DE SOPORTE INTERNET DE LA BASE")
                resultado_soporte_internet = ejecutar_script("extraccion_datos_base_soporte_internet.py")
                
                if resultado_soporte_internet == 0:
                    print("audios Extraidos..")
                    guia = 'guia_set_9'
                    tipo = 'soporte'
                    print(guia)
                    print(tipo)
                else:
                    print("Soporte Internet vacia procedeiendo con Soporte Telefonia")
                    print("\nEXTRAYENDO DATOS DE soporte telefonia DE LA BASE")
                    resultado_soporte_telefonia = ejecutar_script("extraccion_datos_base_soporte_telefonia.py")
                    
                    if resultado_soporte_telefonia == 0:
                        print("audios Extraidos..")
                        guia = 'guia_set_10'
                        tipo = 'soporte'
                        print(guia)
                        print(tipo)
                    else:
                        print("Soporte Telefonia vacia procedeiendo con Retencion")
                        print("\nEXTRAYENDO DATOS DE RETENCION DE LA BASE")
                        resultado_retencion = ejecutar_script("extraccion_datos_base_retenciones.py")
                        
                        if resultado_retencion == 0:
                            print("audios Extraidos..")
                            guia = 'guia_set_12'
                            tipo = 'retenciones'
                            print(guia)
                            print(tipo)
                        else:
                            print("sin info Tabla de audios para Analizar Vacia")
                            send_msg("Analisis masivo finalizado")
                            try:
                                print("Realizando tabla para reprote")
                                send_msg("Realizando tabla para reprote")
                                subprocess.run(["python", "evitar_duplicado_guia.py", guia])
                                response = requests.get("http://192.168.51.210:1023/DashboardController/insertaIndicadorMesCompleto")
                                if response.status_code == 200:
                                    print("\nPetición GET exitosa: ", response.status_code)
                                    send_msg("tablas realizadas")
                                    print("Analizis Finalizado Esperando Siguiente Horario de ejecucion.....")
                                else:
                                    print("\nError en la petición GET: ", response.status_code)
                                    send_msg(f"\nError en la petición GET: {response.status_code}")
                            except Exception as e:
                                print("\nError al hacer la petición GET: ", str(e))
                            break
                        
        print("\nINICIANDO RESULTADO ASISTENTE\n")
        subprocess.run(["python", "asistente.py", guia])
        
        ruta_principal = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1"
        
        for archivo in os.listdir(ruta_principal):
            if archivo.endswith(".txt"):
                ruta_archivo = os.path.join(ruta_principal, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                clasificacion = re.search(r'(?i)Reclasificaci[oó]n[:\s]*\n?(.+)', contenido)
                if clasificacion:
                    tipo_llamada = clasificacion.group(1).strip()
                    if tipo_llamada.lower() in ['retencion', 'retención', 'cancelación']:
                        guia = "guia_set_12"
                        tipo = 'retenciones'
                    elif tipo_llamada.lower() in ['servicios', 'servicio']:
                        guia = "guia_set_1"
                        tipo = 'servicios'
                    elif tipo_llamada.lower() in ['soporte telefonia']:
                        guia = "guia_set_10"
                        tipo = 'soporte'
                    elif tipo_llamada.lower() in ['soporte internet']:
                        guia = "guia_set_9"
                        tipo = 'soporte'
                    elif tipo_llamada.lower() in ['soporte video']:
                        guia = "guia_set_11"
                        tipo = 'soporte'
                    else:
                        print (f"la guia no se pudo asignar")
                    print(f"Tipo de Llamada: {tipo_llamada}, Guía: {guia}")
                else:
                    print("No se encontró el tipo de llamada en la respuesta.")
                
        print(guia)
        print(tipo)

        print("\nINICIANDO CALCULO DEL TOTAL DE RESULTADO ASISTENTE\n")
        subprocess.run(["python", "resultados_cal.py", guia])
        
        print("\nSUBIENDO DATOS DE CONTEXTO_GENERAL A JUSTIFICACIONES_GUIA\n")
        subprocess.run(["python", "justificacion_penalizacion.py", guia, tipo])
        
        print("\nSUBIENDO DATOS DE CONTEXTO_GENERAL A JUSTIFICACIONES_mariana\n")
        subprocess.run(["python", "justificacion_mariana.py", guia, tipo])
        
        print("\nINICIANDO EMOCIONES\n")
        subprocess.run(["python", "emociones.py"])
        
        print("\nINICIANDO RESUMEN-RENCIDENCIA\n")
        subprocess.run(["python", "extraccion_de_resultados.py"])
        
        print("\nINCINADO SUBIDA A LA BASE\n")
        subprocess.run(["python", "Subida_Base.py", guia])
        
        print("\nINCINADO UPDATE De los registro Procesados\n")
        subprocess.run(["python", "completado.py"])
        
        print("\nLimpiando las carpetas para la siguiente carga\n")
        subprocess.run(["python", "eliminar_datos.py"])
        
        # print("\nFINALIZA ANALISIS MASIVO\n")
        # break
    
def iniciar_proceso():
    """Consulta la base cada 30 minutos y ejecuta el flujo si encuentra registros transcritos."""
    while True:
        print("\nConsultando la base de datos de Mariana...")
        registros_pendientes = consultar_Transcritos()
        
        if registros_pendientes > 30:
            print(f"\nSe encontraron {registros_pendientes} registros con estado 'Transcrito'. Iniciando flujo principal...\n")
            flujo_Principal()
        else:
            print("\nNo se encontraron registros transcritos. Esperando 30 minutos antes de la siguiente consulta...\n")
        
        hora_actual = datetime.datetime.now()
        print(f"Siguiente consulta en 30 min, hora actual: {hora_actual.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1800)



if __name__ == "__main__":
    iniciar_proceso()
    

