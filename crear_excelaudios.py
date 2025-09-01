import pandas as pd

ruta_json = r'C:\Users\Jotzi1\Documents\MySql\audios con su transcipcion2.json'

data = pd.read_json(ruta_json)

ruta_excel = r'C:\Users\Jotzi1\Documents\MySql\audios_con_su_transcripcion2.xlsx'
data.to_excel(ruta_excel, index=False)

print(f'Archivo Excel creado exitosamente en: {ruta_excel}')
