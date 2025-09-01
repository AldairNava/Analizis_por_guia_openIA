print("\n--------- INICIANDO PROCESO DE CARGA DE RESULTADO DE CALIFICACIONES ---------\n")

import mysql.connector
import os
import sys
    

# Obtiene los valores de la tabla de guia
def obtener_valores(guia):
    config = {
        'user': 'root',
        'password': 'thor',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()

        # Escapar el nombre de la tabla
        tabla = f'`{guia}`'
        columnas = ['id_subcategoria', 'nombre_punto']

        # Construir la consulta
        consulta = f"""
        SELECT {', '.join(columnas)} FROM {tabla}
        WHERE nombre_punto <> 'Manejo de Herramientas'
        AND nombre_punto <> 'Groserias';
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        resultados = None
    finally:
        cursor.close()
        conexion.close()
    
    return resultados


#obtiene el valor de las calificaciones
def obtener_fila_por_nombre(guia, archivo):
    config = {
        'user': 'root',
        'password': 'thor',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    conexion = mysql.connector.connect(**config)

    cursor = conexion.cursor()

    tabla = f'calificaciones_{guia}'
    nombre_columna = 'filename'
    carpeta_transcripciones = r'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'

    ruta_archivo = os.path.join(carpeta_transcripciones, archivo)
    filename = os.path.splitext(archivo)[0] + ".mp3"
            
            
    columnas_excluir = ['id_audio', 'filename', 'groserias', 'resultado', 'owner', 'tipo', 'problematica', 'solucion', 'punto_de_vista', 'solucion_prob']

    columnas = [columna for columna in obtener_nombres_columnas(cursor, tabla) if columna not in columnas_excluir]

    consulta = f"SELECT {', '.join(columnas)} FROM {tabla} WHERE {nombre_columna} = %s"

    cursor.execute(consulta, (filename,))

    resultados_fila = cursor.fetchall()

    if resultados_fila:
        print(f"\nValores de la fila con {nombre_columna} = '{filename}':")
        for resultado in resultados_fila:
            print(resultado)
    else:
        print(f"No se encontró ninguna fila con {nombre_columna} = '{filename}'")

    cursor.close()
    conexion.close()
    return resultados_fila

       

#obtiene el nombre de las columnas 
def obtener_nombres_columnas(cursor, tabla):
    consulta = f"SHOW COLUMNS FROM {tabla}"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    return [resultado[0] for resultado in resultados]


#obtiene el inicio de la suma

def obtener_sumas(resultados_emparejados):
    sumas = {}
    
    for resultado in resultados_emparejados:
        clave = resultado[0]
        valor = resultado[2]

        if clave not in sumas:
            sumas[clave] = []

        sumas[clave].append(valor)
    
    return sumas


def imprimir_resultados_emparejados(resultados_emparejados):
    print("\nInciando calculo de calificaciones para guia_set_1 o guia_set_12\n")
    sumas = obtener_sumas(resultados_emparejados)
    suma_cali = 0.0
    diez = 10.0
    cinco = 5.0
    
    for clave, valores in sumas.items():
        if any(val == 0 for val in valores):
            print(f"suma para clave {clave} = 0.0\n")
        else:
            if clave == '8' and all(val > 0 for val in valores):
                print(f"suma para clave {clave} = {cinco}\n")
                suma_cali += 5
            elif clave != '10':
                suma_cali += 10
                print(f"suma para clave {clave} = {diez}\n")
    
    suma_cali = suma_cali + 15
          
    return suma_cali


#### PARA SOPORTE
def imprimir_resultados_emparejados_soporte(resultados_emparejados):
    print("\nInciando calculo de calificaciones para guia_set_9 o guia_set_10 o guia_set_11\n")
    sumas = obtener_sumas(resultados_emparejados)
    suma_cali = 0.0
    diez = 10.0
    cinco = 5.0
    
    for clave, valores in sumas.items():
        if clave == '8' and all(val > 0 for val in valores):
            print(f"suma para clave {clave} = {cinco}\n")
            suma_cali += 5
        elif clave == '7' and any(val > 0 for val in valores):
            print(f"suma para clave {clave} = {diez}\n")
            suma_cali += 10
        elif clave != '10':
            if all(val > 0 for val in valores):
                suma_cali += 10
                print(f"suma para clave {clave} = {diez}\n")
            else:
                print(f"suma para clave {clave} = 0.0\n")
    
    suma_cali = suma_cali + 15
          
    return suma_cali




#actualiza el valor de la calificacion por medio del nombre de la columna
def actualizar_resultado(resultado, valor_columna, guia):
    config = {
        'user': 'root',
        'password': 'thor',
        'host': '192.168.51.210',
        'database': 'audios_dana',
    }

    conexion = mysql.connector.connect(**config)

    cursor = conexion.cursor()

    tabla = f'calificaciones_{guia}'
    columna_resultado = 'resultado'
    nombre_columna = 'filename'

    consulta = f"UPDATE {tabla} SET {columna_resultado} = %s WHERE {nombre_columna} = %s"
    cursor.execute(consulta, (resultado, valor_columna))

    conexion.commit()

    cursor.close()
    conexion.close()


def main(guia):
    resultados_valores = obtener_valores(guia)
    carpeta_transcripciones = r'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'
    archivo_Calificaciones = [f for f in os.listdir(carpeta_transcripciones) if f.endswith('.txt')]

    suma_total_calificaciones = 0.0

    for archivo in archivo_Calificaciones:
        resultados_fila = obtener_fila_por_nombre(guia, archivo)

        if resultados_fila:
            resultados_emparejados = [(str(valores[0]), str(valores[1]), resultados_fila[0][i]) for i, valores in enumerate(resultados_valores)]
            
            print("Resultados emparejados para", archivo, ":")
            
            
            #SUMA DE SERVICIOS Y RETENCIONES
            if guia == 'guia_set_1' or guia == 'guia_set_12':
                suma_cali = imprimir_resultados_emparejados(resultados_emparejados)
                suma_total_calificaciones += suma_cali
                
                filename = os.path.splitext(archivo)[0] + ".mp3"
                actualizar_resultado(suma_cali, filename, guia)
            
            #SUMA DE SOPORTE
            elif guia == 'guia_set_9' or guia == 'guia_set_10' or guia == 'guia_set_11':
                suma_cali = imprimir_resultados_emparejados_soporte(resultados_emparejados)
                suma_total_calificaciones += suma_cali
                
                filename = os.path.splitext(archivo)[0] + ".mp3"
                actualizar_resultado(suma_cali, filename, guia)
        else:
            print(f"No se encontró ninguna fila para el archivo {archivo} en la base de datos.")

    print(f"Suma total de calificaciones: {suma_total_calificaciones}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        main(guia)
    else:
        print("Por favor, proporciona el nombre del archivo como argumento de línea de comandos.")
    
    print("═"*30, " Calificacion terminada con exito ", "═"*30)
    
    
    # HACER EL PROCESO MANUAL
    # guia = 'guia_set_12'
    # main(guia)
