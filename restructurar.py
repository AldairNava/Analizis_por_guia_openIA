import os
import json

folder_path = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1"

files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

for file_name in files:
    file_path = os.path.join(folder_path, file_name)


    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()


    lines = content.split('\n')
    data = {}
    for line in lines:
        if '|' in line:
            parts = line.split('|')
            if len(parts) > 2:
                key = parts[1].strip()
                value = parts[2].strip()
                if key and value and key != 'Parametro' and value != 'Calificacion':
                    try:
                        data[key] = int(value)
                    except ValueError:
                        pass 


    json_data = json.dumps(data, indent=2, ensure_ascii=False)


    new_content = f"```json\n{json_data}\n```\n\n{content}"


    with open(file_path, 'w', encoding='latin-1') as file:
        file.write(new_content)

    print(f"El archivo {file_name} ha sido actualizado con éxito.")
