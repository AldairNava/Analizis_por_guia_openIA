import os
import re

ruta_principal = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1"
ruta_resumen = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\resumen"
ruta_reincidencias = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\reincidencia"
ruta_insatisfacciones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\insatisfaccion"
ruta_emociones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones"
ruta_solucion = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\solucion"
ruta_motivo = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\motivo_llamada"
ruta_sentimientos = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\sentimientos"
ruta_problematica = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\problematica"
ruta_titular = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\titularidad"
ruta_datos_actualizacion = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\datos_actualizcion"

os.makedirs(ruta_resumen, exist_ok=True)
os.makedirs(ruta_reincidencias, exist_ok=True)
os.makedirs(ruta_insatisfacciones, exist_ok=True)
os.makedirs(ruta_emociones, exist_ok=True)
os.makedirs(ruta_solucion, exist_ok=True)
os.makedirs(ruta_motivo, exist_ok=True)
os.makedirs(ruta_sentimientos, exist_ok=True)
os.makedirs(ruta_problematica, exist_ok=True)
os.makedirs(ruta_titular, exist_ok=True)
os.makedirs(ruta_datos_actualizacion, exist_ok=True)

def extraer_informacion_contenido(contenido):
    def buscar_regex(pattern, contenido):
        resultado = re.search(pattern, contenido, re.DOTALL)
        if resultado:
            return resultado.group(1).strip()
        else:
            pattern_siguiente = pattern.replace(r'\n?', r'\n')
            resultado_siguiente = re.search(pattern_siguiente, contenido, re.DOTALL)
            return resultado_siguiente.group(1).strip() if resultado_siguiente else ""

    resumen = buscar_regex(r'(?i)(?:###|####)?\s*ResumenFront[:\s]*\n?(.+?)(?=\n\s*Reincidencia|\n\s*-\s*Reincidencia|\n\s*REINCIDENCIA|REINCIDENCIA)', contenido) or \
              buscar_regex(r'(?i)(?:###|####)?\s*RESUMEN[_\s]*FRONT[:\s]*\n?(.+?)(?=\n\s*Reincidencia|\n\s*-\s*Reincidencia|\n\s*REINCIDENCIA|REINCIDENCIA)', contenido)
    reincidencia = buscar_regex(r'(?i)(?:###|####)?\s*Reincidencia[:\s]*\n?(\d+)', contenido)
    insatisfaccion = buscar_regex(r'(?i)(?:###|####)?\s*Insatisfacci[oó]n[:\s]*\n?(\d+)', contenido)
    emocion = buscar_regex(r'(?i)(?:###|####)?\s*Explicaci[oó]n Emocional[:\s]*\n?(.+?)(?=\n(?:###|####)?\s*Llamada Cortada|\Z)', contenido)
    motivo = buscar_regex(r'(?i)Motivo de la llamada[:\s]*\n?(.+?)(?=\n\s*SOLUCION[:\s]*)', contenido)
    solucion = buscar_regex(r'(?i)Solucion[:\s]*\n?(.+?)(?=\n\s*SENTIMIENTOS[:\s]*)', contenido)
    sentimientos = buscar_regex(r'(?i)Sentimientos[:\s]*\n?(.*?)(?=\n*TENDENCIAS)', contenido)
    problematica = buscar_regex(r'(?i)(?:###|####)?\s*PROBLEMATICA[:\s]*\n?(.+?)(?=\n\s*EFICIENCIA|\n\s*eficiencia)', contenido) or \
                   buscar_regex(r'(?i)(?:###|####)?\s*problematicas?[:\s]*\n?(.+?)(?=\n\s*EFICIENCIA|\n\s*eficiencia)', contenido) or \
                   buscar_regex(r'(?i)(?:###|####)?\s*problematica[:\s]*\n?(.+?)(?=\n\s*EFICIENCIA|\n\s*eficiencia)', contenido)
    titular = buscar_regex(r'(?i)Confirmaci[oó]n[\s-]*de[\s-]*titular[:\s]*\n?(.+?)(?=\n\s*MOTIVO[:\s]*)', contenido)
    datos_actualizacion = buscar_regex(r'(?i)-?\s*DATOS\s*DE\s*ACTUALIZACI[oó]N[:\s]*\n?(.+?)(?=\n\s*REINCIDENCIA[:\s]*)', contenido)

    print("Información extraída:")
    print("Resumen:", "Encontrado" if resumen else "No encontrado")
    print("Reincidencia:", "Encontrado" if reincidencia else "No encontrado")
    print("Insatisfacción:", "Encontrado" if insatisfaccion else "No encontrado")
    print("Emoción:", "Encontrado" if emocion else "No encontrado")
    print("Motivo:", "Encontrado" if motivo else "No encontrado")
    print("Solución:", "Encontrado" if solucion else "No encontrado")
    print("Sentimientos:", "Encontrado" if sentimientos else "No encontrado")
    print("Problematica:", "Encontrado" if problematica else "No encontrado")
    print("Titular:", "Encontrado" if titular else "No encontrado")
    print("datos_actualizacion:", "Encontrado" if datos_actualizacion else "No encontrado")

    return {
        "resumen": resumen,
        "reincidencia": reincidencia,
        "insatisfaccion": insatisfaccion,
        "emocion": emocion,
        "motivo": motivo,
        "solucion": solucion,
        "sentimientos": sentimientos,
        "problematica": problematica,
        "titular": titular,
        "datos_actualizacion": datos_actualizacion
    }

def guardar_datos(nombre_archivo, datos):
    print(f"\nGuardando datos para el archivo: {nombre_archivo}")

    with open(os.path.join(ruta_resumen, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["resumen"])
        print(f"Resumen guardado en {ruta_resumen}")

    with open(os.path.join(ruta_reincidencias, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["reincidencia"])
        print(f"Reincidencia guardada en {ruta_reincidencias}")

    with open(os.path.join(ruta_insatisfacciones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["insatisfaccion"])
        print(f"Insatisfacción guardada en {ruta_insatisfacciones}")

    with open(os.path.join(ruta_emociones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["emocion"])
        print(f"Emoción guardada en {ruta_emociones}")

    with open(os.path.join(ruta_motivo, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["motivo"])
        print(f"Motivo guardado en {ruta_motivo}")

    with open(os.path.join(ruta_solucion, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["solucion"])
        print(f"Solución guardada en {ruta_solucion}")

    with open(os.path.join(ruta_sentimientos, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["sentimientos"])
        print(f"Sentimientos guardados en {ruta_sentimientos}")

    with open(os.path.join(ruta_problematica, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["problematica"])
        print(f"problematica guardados en {ruta_problematica}")

    with open(os.path.join(ruta_titular, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["titular"])
        print(f"titular guardados en {ruta_titular}")

    with open(os.path.join(ruta_datos_actualizacion, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["datos_actualizacion"])
        print(f"datos de actualizacion guardados en {ruta_datos_actualizacion}")

for archivo in os.listdir(ruta_principal):
    if archivo.endswith(".txt"):
        print(f"\nProcesando archivo: {archivo}")
        ruta_archivo = os.path.join(ruta_principal, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        datos_extraidos = extraer_informacion_contenido(contenido)
        guardar_datos(archivo, datos_extraidos)

print("\nAnálisis completado.")
