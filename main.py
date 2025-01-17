import subprocess
import datetime
import schedule
import requests
import time
import re
import os
from Tele import send_msg

def ejecutar_script(script):
    resultado = subprocess.run(["python", script], capture_output=True, text=True)
    return resultado.returncode

def flujo_Principal():
    # send_msg("Analizis Masivo Iniciado")
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
                            # send_msg("Analisis masivo finalizado")
                            try:
                                print("Realizando tabla para reprote")
                                # send_msg("Realizando tabla para reprote")
                                response = requests.get("http://192.168.51.210/api/DashboardController/insertaIndicadorMesCompleto")
                                if response.status_code == 200:
                                    print("\nPetición GET exitosa: ", response.status_code)
                                    print("Analizis Finalizado Esperando Siguiente Horario de ejecucion.....")
                                else:
                                    print("\nError en la petición GET: ", response.status_code)
                            except Exception as e:
                                print("\nError al hacer la petición GET: ", str(e))
                            break
                        
        print("\nINICIANDO RESULTADO ASISTENTE\n")
        subprocess.run(["python", "asistente.py", guia])
        # time.sleep(100000)
        
        ruta_principal = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\calificacion\pov1"
        
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
                    elif tipo_llamada.lower() in ['servicios']:
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
        
        # print("\nINCINADO SUBIDA DATOS FALTANTES\n")
        # subprocess.run(["python", "insercion_datos_faltantes.py", guia])
        
        print("\nINCINADO UPDATE De los registro Procesados\n")
        subprocess.run(["python", "completado.py"])
        
        print("\nLimpiando las carpetas para la siguiente carga\n")
        subprocess.run(["python", "eliminar_datos.py"])
        
        print("\nFINALIZA ANALISIS MASIVO\n")
        # break

def main():
    print("esperando Horario de Ejecucion analizis mariana....")
    schedule.every().day.at("06:00").do(flujo_Principal)
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    # main()
    flujo_Principal()
    

