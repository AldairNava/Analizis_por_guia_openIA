import os
import re
import mysql.connector
import sys

# Lista de categorías
parametros_categorias = {
    "Script_entrada": "Apertura_y_Cierre",
    "Script_salida": "Apertura_y_Cierre",
    "Transferencia": "Apertura_y_Cierre",
    "Presta_atencion_al_cliente": "Habilidades_Escucha_Comunicacion",
    "Utiliza_palabras_entendibles": "Habilidades_Escucha_Comunicacion",
    "Se_dirige_apropiadamente": "Cortesia_y_Etiqueta",
    "Utiliza_frases_de_cortesia": "Cortesia_y_Etiqueta",
    "Ofrece_disculpa_ante_reclamo": "Cortesia_y_Etiqueta",
    "Preguntas_sin_responder": "Cortesia_y_Etiqueta",
    "Informa_tiempos_de_espera": "Cortesia_y_Etiqueta",
    "No_hace_comentarios_innecesarios": "Cortesia_y_Etiqueta",
    "Atiende_la_llamada": "Manejo_de_Tiempos",
    "Validacion_de_datos": "Validacion_de_Datos",
    "Sondeo_al_cliente": "Sondeo_y_Analisis",
    #APEGO A POLITICAS
    
    "Objecciones": "Apego_a_Politicas_y_Procediminetos",
    "Objeciones": "Apego_a_Politicas_y_Procediminetos",
    "Consulta_de_saldo": "Apego_a_Politicas_y_Procediminetos",
    
    'Fecha_solicitada': "Apego_a_Politicas_y_Procediminetos",
    'Horario_de_atencion': "Apego_a_Politicas_y_Procediminetos",
    'Numero_de_orden': "Apego_a_Politicas_y_Procediminetos",
    'Solicitud_tecnico': "Apego_a_Politicas_y_Procediminetos",
    'Validar_numero_telefonico': "Apego_a_Politicas_y_Procediminetos",
    
    'Numero_de_orden': "Apego_a_Politicas_y_Procediminetos",
    'Descuento_reflejado': "Apego_a_Politicas_y_Procediminetos",
    'Informar_de_incumplimiento': "Apego_a_Politicas_y_Procediminetos",
    'Entrega_de_formato': "Apego_a_Politicas_y_Procediminetos",
    
    'Inconsistencias_facturacion': "Apego_a_Politicas_y_Procediminetos",
    'Inconsistencias_facturacion_solucion': "Apego_a_Politicas_y_Procediminetos",
    'Numero_telefonico': "Apego_a_Politicas_y_Procediminetos",
    'Correo_electronico': "Apego_a_Politicas_y_Procediminetos",
    'Numero_de_reporte': "Apego_a_Politicas_y_Procediminetos",
    'Aumento_tarifa': "Apego_a_Politicas_y_Procediminetos",
    'Activo_no_instalado': "Apego_a_Politicas_y_Procediminetos",
    'Informacion_aumento': "Apego_a_Politicas_y_Procediminetos",
    'Cambio_o_venta': "Apego_a_Politicas_y_Procediminetos",
    'canalizar': "Apego_a_Politicas_y_Procediminetos",
    'Productos_comprar': "Apego_a_Politicas_y_Procediminetos",
    
    'Cambio_de_correo': "Apego_a_Politicas_y_Procediminetos",
    'Validacion_de_titularidad': "Apego_a_Politicas_y_Procediminetos",
    'Validacion_de_titularidad2': "Apego_a_Politicas_y_Procediminetos",
    
    'Regla_1': "Apego_a_Politicas_y_Procediminetos",
    'Regla_2': "Apego_a_Politicas_y_Procediminetos",
    'Regla_3': "Apego_a_Politicas_y_Procediminetos",
    'Regla_4': "Apego_a_Politicas_y_Procediminetos",
    'DOWNGRADE_DOWNSALE': "Apego_a_Politicas_y_Procediminetos",
    'Reduccion_izzi_20': "Apego_a_Politicas_y_Procediminetos",
    
    'Regla_1': "Apego_a_Politicas_y_Procediminetos",
    'Regla_2': "Apego_a_Politicas_y_Procediminetos",
    'Regla_3': "Apego_a_Politicas_y_Procediminetos",
    'Regla_4': "Apego_a_Politicas_y_Procediminetos",
    'UPGRADE_UPSALE': "Apego_a_Politicas_y_Procediminetos",
    
    'Soporte_internet_alambrico': "Apego_a_Politicas_y_Procediminetos",
    'Soporte_internet_inalambrico': "Apego_a_Politicas_y_Procediminetos",
    'Visita_tecnica': "Apego_a_Politicas_y_Procediminetos",
    
    'Soporte_telefonia': "Apego_a_Politicas_y_Procediminetos",
    'Visita_tecnica': "Apego_a_Politicas_y_Procediminetos",
    
    'Soporte_video': "Apego_a_Politicas_y_Procediminetos",
    'Visita_tecnica': "Apego_a_Politicas_y_Procediminetos",
    
    'Retencion':  "Apego_a_Politicas_y_Procediminetos",
    
    "Recapitulacion_de_proceso": "Solucion_y_Confirmacion_de_Acuerdos",
    "Aclaracion_de_dudas": "Manejo_de_Informacion",
    
    "groserias": "groserias",
    "Groserias": "groserias"

}

parametros_categorias_base = {
    "Apertura_y_Cierre",
    "Habilidades_Escucha_Comunicacion",
    "Cortesia_y_Etiqueta",
    "Manejo_de_Tiempos",
    "Validacion_de_Datos",
    "Sondeo_y_Analisis",
    "Apego_a_Politicas_y_Procediminetos",
    "Solucion_y_Confirmacion_de_Acuerdos",
    "Manejo_de_Informacion",
    "groserias"
}

# Función para extraer los datos de la tabla del archivo .txt
def extract_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.findall(r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', content, re.DOTALL)
        penalizations = {}
        for match in matches:
            parameter, _, _, justification = match  # Ajusta la asignación para capturar el campo de justificación
            if parameter == 'Groserias':
                parameter = 'groserias'  # Modifica 'Groserias' a 'groserias'
            category = parametros_categorias.get(parameter, None)
            if category and justification.strip():
                penalizations.setdefault(category, []).append(justification.strip())  # Solo captura la descripción de la penalización
        return penalizations


    
def main(guia, tipo):
    # Conexión a la base de datos MySQL
    db_connection = mysql.connector.connect(
        host="192.168.51.210",
        user="root",
        password="",
        database="audios_dana"
    )

    # Cursor para ejecutar las consultas SQL
    cursor = db_connection.cursor()

    # Ruta de la carpeta local donde se encuentran los archivos .txt
    folder_path = r"C:\Users\Jotzi1\Desktop\copias\Analisis_por_guia\Proceso_Clidad_1\contextos_calidad"

    # Lista para almacenar los datos a insertar en la base de datos
    data_to_insert = []

    # Iterar sobre los archivos .txt en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            penalizations = extract_data_from_file(file_path)
            data_tuple = [filename[:-4] + ".mp3"]  # Empezamos con el nombre de archivo
            for category in parametros_categorias_base:
                # Si hay penalizaciones para esta categoría, agregamos la descripción de la penalización
                if category in penalizations:
                    # Solo tomamos la primera descripción de penalización si hay varias
                    description = penalizations[category][0] if penalizations[category] else None
                    data_tuple.append(description)
                else:
                    # Si no hay penalizaciones para esta categoría, agregamos NULL
                    data_tuple.append(None)
            # Finalmente, agregamos los valores constantes para owner, guia y tipo
            data_tuple.extend(["izzi", guia, tipo])
            data_to_insert.append(data_tuple)



    # Lista de nombres de columnas para la consulta SQL
    column_names = ["filename"] + list(parametros_categorias_base) + ["owner", "guia", "tipo"]

    # Consulta SQL para insertar los datos en la tabla
    sql = "INSERT INTO justificacion_mariana ({}) VALUES ({})".format(", ".join(column_names), ", ".join(["%s"] * len(column_names)))

    # Imprimir consulta SQL para depuración
    print("Consulta SQL:", sql)

    # Imprimir datos a insertar para depuración
    print("Datos a insertar:", data_to_insert)

    # Ejecutar la consulta para insertar los datos
    cursor.executemany(sql, data_to_insert)

    # Confirmar la transacción
    db_connection.commit()

    # Cerrar conexión y cursor
    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        guia = sys.argv[1]
        tipo = sys.argv[2]
        main(guia, tipo)