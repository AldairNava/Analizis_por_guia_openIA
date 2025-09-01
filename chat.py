import os
import assemblyai as aai
import multiprocessing

assemblyai_api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = assemblyai_api_key

CARPETA_AUDIOS = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\audios"
CARPETA_SALIDA_CHAT = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\chat"
CARPETA_SALIDA_TRANSCRIPCION = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones"

def transcribir_audio(archivo_audio):
    transcriptor = aai.Transcriber()
    configuracion = aai.TranscriptionConfig(speaker_labels=True, speech_model=aai.SpeechModel.nano)
    
    try:
        transcripcion = transcriptor.transcribe(archivo_audio, config=configuracion)
        if transcripcion is None:  # Verificación de transcripción
            print(f"Error: Transcripción fallida para {archivo_audio}")
            return
        
        nombre_archivo = os.path.splitext(os.path.basename(archivo_audio))[0]
        archivo_salida_chat = os.path.join(CARPETA_SALIDA_CHAT, f"{nombre_archivo}.txt")
        archivo_salida_transcripcion = os.path.join(CARPETA_SALIDA_TRANSCRIPCION, f"{nombre_archivo}.txt")
        
        with open(archivo_salida_chat, "w", encoding='utf-8') as archivo_chat, \
             open(archivo_salida_transcripcion, "w", encoding='utf-8') as archivo_transcripcion:
            for turno in transcripcion.utterances:
                etiqueta_speaker = turno.speaker
                if etiqueta_speaker == 'A' or etiqueta_speaker == 'C':
                    etiqueta_speaker_transcripcion = 'A.T.'
                elif etiqueta_speaker == 'B' or etiqueta_speaker == 'D':
                    etiqueta_speaker_transcripcion = 'C.'
                archivo_chat.write(f"{etiqueta_speaker_transcripcion}: {turno.text}\n")
                archivo_transcripcion.write(f"{etiqueta_speaker}: {turno.text.replace('A:', '').replace('B:', '').replace('C:', '').replace('D:', '')}\n")
    except Exception as e:  # Manejo de excepciones
        print(f"Error en la transcripción de {archivo_audio}: {e}")

if __name__ == "__main__":
    # nombre_archivo="TVTET9O69968NAFB4RCN76HPD803D831.mp3"
    archivos_audio = [os.path.join(CARPETA_AUDIOS, nombre_archivo) for nombre_archivo in os.listdir(CARPETA_AUDIOS) if nombre_archivo.endswith(".mp3")]
    grupo_procesos = multiprocessing.Pool()
    grupo_procesos.map(transcribir_audio, archivos_audio)
    grupo_procesos.close()
    grupo_procesos.join()
