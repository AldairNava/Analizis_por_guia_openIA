print("\n--------- INICIANDO OBTENCION DE EMOCIONES ---------\n")

import os
import glob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def emociones_dato():
    nltk.download('vader_lexicon')

    def transcribe_text(text_path):
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

    results_folder = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\emociones'
    os.makedirs(results_folder, exist_ok=True)

    text_paths = glob.glob(folder_path + '/*.txt')

    sia = SentimentIntensityAnalyzer()

    for text_path in text_paths:

        file_name = os.path.splitext(os.path.basename(text_path))[0]


        result_file = os.path.join(results_folder, file_name + '.txt')
        if os.path.exists(result_file):
            print(f"El archivo {file_name} ya ha sido analizado.")
            continue


        text = transcribe_text(text_path)


        secciones = descomponer_prompt(text, 4090)


        scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
        for seccion in secciones:
            sentiment_scores = sia.polarity_scores(seccion)

            scores['neg'] += sentiment_scores['neg']
            scores['neu'] += sentiment_scores['neu']
            scores['pos'] += sentiment_scores['pos']
            scores['compound'] += sentiment_scores['compound']


        num_secciones = len(secciones)
        scores['neg'] /= num_secciones
        scores['neu'] /= num_secciones
        scores['pos'] /= num_secciones
        scores['compound'] /= num_secciones


        max_emotion = max(scores['neg'], scores['neu'], scores['pos'])
        scores['neg'] = 1 if scores['neg'] == max_emotion else 0
        scores['neu'] = 1 if scores['neu'] == max_emotion else 0
        scores['pos'] = 1 if scores['pos'] == max_emotion else 0

        print(f"Análisis de sentimientos del archivo de texto: {file_name}")
        print(f"Puntuación de negatividad: {scores['neg']}")
        print(f"Puntuación de neutralidad: {scores['neu']}")
        print(f"Puntuación de positividad: {scores['pos']}\n")
        print(f"Puntuación de sentimiento general: {scores['compound']}\n")


        with open(result_file, 'w') as file:
            file.write(f"Análisis de sentimientos del archivo de texto: {file_name}\n")
            file.write(f"Puntuación de negatividad: {scores['neg']}\n")
            file.write(f"Puntuación de neutralidad: {scores['neu']}\n")
            file.write(f"Puntuación de positividad: {scores['pos']}\n")
            file.write(f"Puntuación de sentimiento general: {scores['compound']}\n")


def descomponer_prompt(texto, longitud_maxima):
    secciones = []

    while len(texto) > longitud_maxima:

        indice_punto = texto.rfind('.', 0, longitud_maxima)


        if (indice_punto != -1):
    
            seccion = texto[:indice_punto + 1]
            secciones.append(seccion)
            texto = texto[indice_punto + 1:].lstrip()
        else:
    
            seccion = texto[:longitud_maxima]
            secciones.append(seccion)
            texto = texto[longitud_maxima:].lstrip()

    secciones.append(texto)

    return secciones

if __name__ == "__main__":
    emociones_dato()
    print("\n--------- FINALIZA OBTENCION DE EMOCIONES CON EXITO ---------\n")
