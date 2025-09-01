import os
import mysql.connector

def transcripciones():
    print("\nInciando validacion de la columna transcripcion")
    db_config = {
        'host': '192.168.51.210',
        'user': 'root',
        'password': 'thor',
        'database': 'audios_dana'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

    query = """
    SELECT id_audio, filename 
    FROM prueba_dana_calidad 
    WHERE transcripcion IS NULL OR transcripcion = ''
    ORDER BY id_audio DESC ;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        id_audio, filename = record

        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(folder_path, f"{base_filename}.txt")
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                transcription = file.read()
            
        
            update_query = """
            UPDATE prueba_dana_calidad 
            SET transcripcion = %s 
            WHERE id_audio = %s;
            """
            cursor.execute(update_query, (transcription, id_audio))
            conn.commit()
            print(f"Transcripción actualizada para id_audio: {id_audio}")
        else:
            print(f"Archivo no encontrado para: {filename}")

    cursor.close()
    conn.close()
    
    
    
    
def chat():
    print("\nInciando validacion de la columna chat")
    db_config = {
        'host': '192.168.51.210',
        'user': 'root',
        'password': 'thor',
        'database': 'audios_dana'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\chat'

    query = """
    SELECT id_audio, filename 
    FROM prueba_dana_calidad 
    WHERE chat IS NULL OR chat = ''
    ORDER BY id_audio DESC ;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        id_audio, filename = record

        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(folder_path, f"{base_filename}.txt")
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                chat = file.read()
            
        
            update_query = """
            UPDATE prueba_dana_calidad 
            SET chat = %s 
            WHERE id_audio = %s;
            """
            cursor.execute(update_query, (chat, id_audio))
            conn.commit()
            print(f"Chat actualizada para id_audio: {id_audio}")
        else:
            print(f"Archivo no encontrado para: {filename}")

    cursor.close()
    conn.close()





def transcripcion_original():
    print("\nInciando validacion de la columna transcripcion_original")
    db_config = {
        'host': '192.168.51.210',
        'user': 'root',
        'password': 'thor',
        'database': 'audios_dana'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

    query = """
    SELECT id_audio, filename 
    FROM prueba_dana_calidad 
    WHERE transcripcion_original IS NULL OR transcripcion_original = ''
    ORDER BY id_audio DESC ;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        id_audio, filename = record

        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(folder_path, f"{base_filename}.txt")
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                transcription = file.read()
            
        
            update_query = """
            UPDATE prueba_dana_calidad 
            SET transcripcion_original = %s 
            WHERE id_audio = %s;
            """
            cursor.execute(update_query, (transcription, id_audio))
            conn.commit()
            print(f"Transcripción actualizada para id_audio: {id_audio}")
        else:
            print(f"Archivo no encontrado para: {filename}")

    cursor.close()
    conn.close()
    




def justificacion_emociones():
    print("\nInciando validacion de la columna justificacion_emociones")
    db_config = {
        'host': '192.168.51.210',
        'user': 'root',
        'password': 'thor',
        'database': 'audios_dana'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones'

    query = """
    SELECT id_audio, filename 
    FROM prueba_dana_calidad 
    WHERE justificacion_emociones IS NULL OR justificacion_emociones = ''
    ORDER BY id_audio DESC ;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        id_audio, filename = record

        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(folder_path, f"{base_filename}.txt")
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='latin-1') as file:
                justificacion_emociones = file.read()
            
        
            update_query = """
            UPDATE prueba_dana_calidad 
            SET justificacion_emociones = %s 
            WHERE id_audio = %s;
            """
            cursor.execute(update_query, (justificacion_emociones, id_audio))
            conn.commit()
            print(f"Transcripción actualizada para id_audio: {id_audio}")
        else:
            print(f"Archivo no encontrado para: {filename}")

    cursor.close()
    conn.close()




def resumen():
    print("\nInciando validacion de la columna resumen")
    
    db_config = {
        'host': '192.168.51.210',
        'user': 'root',
        'password': 'thor',
        'database': 'audios_dana'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    folder_path = r'C:\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones'

    query = """
    SELECT id_audio, filename 
    FROM contextos_calidad 
    WHERE resumen IS NULL OR resumen = ''
    ORDER BY id_audio DESC ;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for record in results:
        id_audio, filename = record

        base_filename = os.path.splitext(filename)[0]
        file_path = os.path.join(folder_path, f"{base_filename}.txt")
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='latin-1') as file:
                resumen = file.read()
            
        
            update_query = """
            UPDATE contextos_calidad 
            SET resumen = %s 
            WHERE id_audio = %s;
            """
            cursor.execute(update_query, (resumen, id_audio))
            conn.commit()
            print(f"Transcripción actualizada para id_audio: {id_audio}")
        else:
            print(f"Archivo no encontrado para: {filename}")

    cursor.close()
    conn.close()
    
    
    
    
    

if __name__ == '__main__':
    transcripciones()
    chat()
    transcripcion_original()
    justificacion_emociones()
    resumen()