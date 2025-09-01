import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

def select_audios_del_dia():
    # Establecer conexión a la base de datos
    try:
        connection = mysql.connector.connect(
            host="192.168.51.210",
            user="root",
            password="thor",
            database="audios_dana",
            connection_timeout=90  # Establece un tiempo de espera de 90 segundos
        )
        cursor = connection.cursor()
        print("Conexión establecida correctamente.")
        
        # Obtener la fecha de ayer
        ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Consulta SQL para obtener los registros del día de ayer
        query = f"SELECT * FROM audios WHERE DATE(created_at) = '{ayer}'"
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        print(resultados)
        # Imprimir resultados
        print(f"Resultados de la consulta para la fecha {ayer}:")
        for resultado in resultados:
            print(resultado)
        
        cursor.close()
        connection.close()
        print("Conexión cerrada correctamente.")
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Nombre de usuario o contraseña incorrectos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(f"Error al conectar a la base de datos: {err}")

if __name__ == "__main__":
    select_audios_del_dia()
