import os

def eliminar_archivos_en_carpetas(carpetas):
    for carpeta in carpetas:
        
        archivos = os.listdir(carpeta)

        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_completa):
                try:
                    os.remove(ruta_completa)
                    print(f"Se ha eliminado el archivo: {ruta_completa}")
                except Exception as e:
                    print(f"No se pudo eliminar {ruta_completa}: {e}")

def elim():
    carpetas = [
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\audios",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\audios_extraidos",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov2",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov3",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov4",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_1",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\json_calificacion_2",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\chat",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\contextos_calidad",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\emociones",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\insatisfaccion",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\nombre_audios",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\reincidencia",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\resumen",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\solucion",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\motivo_llamada",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\sentimientos",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\problematica",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\titularidad",
        r"C:\Analisis_Masivo_guia\Proceso_Clidad_1\datos_actualizcion",
    ]

    eliminar_archivos_en_carpetas(carpetas)

if __name__ == "__main__":
    print("\n--------- INICIANDO ELIMINACION DE ARCHIVOS ALMACENADOS ---------\n")
    elim()
    print("\n--------- FINALIZA ELIMINACION CON EXITO ---------\n")