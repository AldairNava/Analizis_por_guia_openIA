import os
import re

ruta_principal = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\calificacion\pov1"
ruta_resumen = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\resumen"
ruta_reincidencias = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\reincidencia"
ruta_insatisfacciones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\insatisfaccion"
ruta_emociones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\justificacion_emociones"

os.makedirs(ruta_resumen, exist_ok=True)
os.makedirs(ruta_reincidencias, exist_ok=True)
os.makedirs(ruta_insatisfacciones, exist_ok=True)
os.makedirs(ruta_emociones, exist_ok=True)

def extraer_informacion_contenido(contenido):
    resumen = re.search(r'(?i)(?:###|####)?\s*Resumen[:\s]*\n?(.+?)(?=\n\s*Reincidencia)', contenido, re.DOTALL)
    reincidencia = re.search(r'(?i)(?:###|####)?\s*Reincidencia[:\s]*\n?(\d+)', contenido)
    insatisfaccion = re.search(r'(?i)(?:###|####)?\s*Insatisfacción[:\s]*\n?(\d+)', contenido)
    emocion = re.search(r'(?i)(?:###|####)?\s*Explicación Emocional[:\s]*\n?(.+?)(?=\n(?:###|####)?\s*Llamada Cortada|\Z)', contenido, re.DOTALL)


    return {
        "resumen": resumen.group(1).strip() if resumen else "",
        "reincidencia": reincidencia.group(1).strip() if reincidencia else "",
        "insatisfaccion": insatisfaccion.group(1).strip() if insatisfaccion else "",
        "emocion": emocion.group(1).strip() if emocion else ""
    }

def guardar_datos(nombre_archivo, datos):

    with open(os.path.join(ruta_resumen, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["resumen"])


    with open(os.path.join(ruta_reincidencias, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["reincidencia"])


    with open(os.path.join(ruta_insatisfacciones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["insatisfaccion"])


    with open(os.path.join(ruta_emociones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["emocion"])

for archivo in os.listdir(ruta_principal):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(ruta_principal, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

    
        datos_extraidos = extraer_informacion_contenido(contenido)

    
        guardar_datos(archivo, datos_extraidos)

print("Análisis completado.")
