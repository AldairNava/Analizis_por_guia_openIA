import mysql.connector
import os
from ftplib import FTP

db_config = {
    'host': '192.168.51.210',
    'user': 'root',
    'password': 'thor',
    'database': 'audios_dana'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

query = """
    SELECT audio_name 
    FROM audios 
    WHERE owner = 'izzi' 
    AND status = 'Pendiente';
"""
cursor.execute(query)
result = cursor.fetchall()

audio_names_db = [row[0] for row in result]

ftp_config = {
    'host': '192.168.50.37',
    'user': 'rpaback1',
    'passwd': 'Cyber123'
}

ftp = FTP()
ftp.connect(ftp_config['host'])
ftp.login(ftp_config['user'], ftp_config['passwd'])

ftp.cwd('Audios')

audio_files_ftp = ftp.nlst()

missing_files = [audio for audio in audio_names_db if audio not in audio_files_ftp]

if missing_files:
    print("Archivos faltantes en la carpeta FTP:")
    for file in missing_files:
        print(file)
else:
    print("Todos los archivos están presentes en la carpeta FTP.")

cursor.close()
conn.close()
ftp.quit()
