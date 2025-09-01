Documentación MarIAna

Este programa utiliza algoritmos avanzados de inteligencia artificial para analizar y procesar archivos de audio de manera automatizada y eficiente. Su objetivo principal es extraer información valiosa a partir del contenido sonoro, facilitando la interpretación y categorización de datos acústicos en diversos contextos.

Funcionalidades clave:
Transcripción automática: Convierte el habla en texto de manera precisa, permitiendo realizar búsquedas y análisis sobre el contenido transcrito.

Identificación de patrones: El programa puede detectar palabras clave, frases repetitivas o patrones de voz que ayuden a clasificar los audios por temáticas, emociones, o intenciones.

Reconocimiento de emociones: Utilizando redes neuronales, el sistema es capaz de identificar el tono emocional del hablante, como alegría, tristeza, enojo, entre otros.

Detección de ruido: El programa analiza la calidad del audio y es capaz de identificar y aislar ruidos de fondo, mejorando la claridad de la señal de voz principal.

Análisis de timbre y tono de voz: Ofrece un estudio detallado del tono, el timbre, la cadencia, y otros aspectos del habla que pueden ser útiles en la caracterización del hablante.

Análisis de sentimiento: Mediante modelos de procesamiento de lenguaje natural (NLP), el sistema puede realizar un análisis de sentimiento, especialmente útil en audios de interacciones comerciales o estudios de mercado.


Usos:
Atención al cliente: Monitoreo de conversaciones para detectar problemas comunes, analizar la calidad del servicio y medir la satisfacción del cliente.

Ventajas:
Alta precisión: Utiliza técnicas de machine learning para mejorar la exactitud a medida que procesa más audios.
Automatización: Reduce el tiempo de análisis y transcripción de audios, incrementando la eficiencia operativa.
Escalabilidad: Puede manejar grandes volúmenes de datos de audio, lo que lo hace ideal para empresas de cualquier tamaño.
Este programa está diseñado para adaptarse a diferentes industrias, proporcionando una solución completa para el análisis de audios mediante IA, con capacidades de personalización según las necesidades del usuario.




################################### DESCRIPCION CODIGO MAIN

## Descripción General
Este script es un programa de procesamiento por lotes que realiza una serie de tareas relacionadas con la extracción, procesamiento y análisis de datos de audio. El script está diseñado para ejecutar 30 iteraciones, cada una procesando diferentes conjuntos de datos basados en el número de iteración.

Importaciones

- subprocess: Utilizado para ejecutar scripts de Python externos.
- requests: Utilizado para realizar una petición HTTP GET al final del proceso.

Función Principal: main()
Estructura del Bucle Principal
El script utiliza un bucle while que se ejecuta 30 veces, con i como contador de iteraciones.
Proceso por Iteración

Extracción de Datos de la Base de Datos

Iteraciones 1-10: Extrae datos de servicio
Iteraciones 11-25: Extrae datos de soporte
Iteraciones 26-30: Extrae datos de retención


Configuración de Variables

guia: Define el conjunto de guías a utilizar
tipo: Define el tipo de datos (servicios, soporte, retenciones)


Ejecución de Scripts

mover_ida.py: mueve o extrae archivos de audio
chat.py: Realiza transcripción y análisis de chat
ajustar_transcripcion.py: Ajusta las transcripciones
asistente.py: Procesa los datos con un asistente virtual
resultados_cal.py: Calcula resultados totales
justificacion_penalizacion.py: Sube datos a una tabla de justificaciones
justificacion_mariana.py: Sube datos a otra tabla de justificaciones
emociones.py: Analiza emociones en los datos
extraccion_de_resultados.py: Genera resúmenes o extrae resultados finales
Subida_Base.py: Sube datos a una base de datos (ejecutado dos veces)
insercion_datos_faltantes.py: Inserta datos faltantes en la base de datos
completado.py: Marca la iteración como completada
eliminar_datos.py: Limpia datos temporales o innecesarios


Finalización del Proceso
Después de completar las 30 iteraciones, el script realiza una petición GET a un servidor local (probablemente para actualizar algún indicador o dashboard).











################################### DESCRIPCION CODIGO EXTRACCION DE DATOS_BASE_SERVICIOS SOPORTE RETENCIONES
## Descripción General
Este script realiza las siguientes operaciones principales:

Se conecta a una base de datos MySQL.
Ejecuta una consulta para obtener nombres de archivos de audio.
Guarda estos nombres en un archivo local.
Se conecta a un servidor FTP.
Descarga los archivos de audio correspondientes desde el servidor FTP.

Importaciones

mysql.connector: Para la conexión y operaciones con la base de datos MySQL.
os: Para operaciones del sistema de archivos.
ftplib.FTP: Para la conexión y operaciones con el servidor FTP.

Funciones
copiar_archivos_desde_ftp(archivos, carpeta_ftp, carpeta_local)
Esta función se encarga de copiar archivos desde un servidor FTP a una carpeta local.
Parámetros:

archivos: Lista de nombres de archivos a copiar.
carpeta_ftp: Ruta de la carpeta en el servidor FTP.
carpeta_local: Ruta de la carpeta local donde se guardarán los archivos.

Proceso:

Se conecta al servidor FTP (IP: 192.168.50.37) con credenciales específicas.
Cambia al directorio FTP especificado.
Para cada archivo en la lista:

Abre un archivo local en modo escritura binaria.
Descarga el archivo desde el FTP y lo escribe en el archivo local.


Cierra la conexión FTP.

Flujo Principal del Script

Conexión a la Base de Datos

Se conecta a una base de datos MySQL en el host 192.168.51.210.


Consulta a la Base de Datos

Ejecuta una consulta SQL para seleccionar nombres de archivos de audio con criterios específicos:

Pertenecientes a 'izzi'
Tipo 'servicios'
Con tarea programada y no analizados


Limita la selección a 30 registros.


Procesamiento de Resultados

Guarda los nombres de los audios en un archivo local 'audios.txt'.


Descarga de Archivos

Llama a la función copiar_archivos_desde_ftp para descargar los archivos de audio del servidor FTP.

Manejo de Errores

Utiliza un bloque try-except para capturar y manejar errores de MySQL.
Imprime mensajes de error específicos en caso de problemas con la base de datos.

Limpieza

Cierra el cursor y la conexión a la base de datos en un bloque finally para garantizar la liberación de recursos.

Notas Adicionales

El script está diseñado para trabajar con una estructura específica de base de datos y FTP.
Se asume que los archivos de audio están en una carpeta llamada "Audios" en el servidor FTP.
Los archivos descargados se guardan en una carpeta local específica.
El script está limitado a procesar 30 archivos de audio por ejecución.





################################### DESCRIPCION CODIGO MOVER_IDA
## Descripción General
Este script de Python se encarga de mover archivos de audio (.mp3 o .wav) de un directorio de origen a un directorio de destino. Si hay más de 30 archivos en el directorio de origen, selecciona aleatoriamente 30 para mover.
Importaciones

os: Para operaciones del sistema de archivos y manipulación de rutas.
shutil: Para operaciones de alto nivel en archivos y colecciones de archivos.
random: Para la selección aleatoria de archivos.

Variables Principales

directorio_origen: Ruta del directorio donde se encuentran originalmente los archivos de audio.
directorio_destino: Ruta del directorio a donde se moverán los archivos de audio.

Proceso Principal

Listar Archivos de Audio

Crea una lista archivos_audio que contiene todos los archivos con extensión .mp3 o .wav en el directorio de origen.
Utiliza una comprensión de lista con la función os.listdir() y verifica las extensiones de los archivos.


Selección de Archivos a Mover

Si hay más de 30 archivos en archivos_audio:

Usa random.sample() para seleccionar aleatoriamente 30 archivos.


Si hay 30 o menos archivos:

Utiliza todos los archivos disponibles.

Mover Archivos

Itera sobre los archivos seleccionados en archivos_a_mover.
Para cada archivo:

Construye la ruta completa de origen y destino usando os.path.join().
Utiliza shutil.move() para mover el archivo del origen al destino.
Imprime un mensaje confirmando el movimiento de cada archivo.








################################### DESCRIPCION CODIGO CHAT
## Descripción General
Este script de Python utiliza la API de AssemblyAI para transcribir archivos de audio MP3. Procesa múltiples archivos en paralelo y genera dos tipos de archivos de salida: uno para chat y otro para transcripción general.
Importaciones

os: Para operaciones del sistema de archivos y variables de entorno.
assemblyai: Para interactuar con la API de AssemblyAI.
multiprocessing: Para procesar múltiples archivos en paralelo.

Configuración

La clave API de AssemblyAI se obtiene de una variable de entorno.
Se definen rutas para las carpetas de entrada y salida.

Función Principal: transcribir_audio(archivo_audio)
Esta función realiza la transcripción de un archivo de audio individual.
Proceso:

Inicializa un transcriptor de AssemblyAI con configuración para etiquetas de hablante y el mejor modelo de habla.
Transcribe el archivo de audio.
Genera nombres de archivo para las salidas de chat y transcripción.
Escribe los resultados en dos archivos diferentes:

Archivo de chat: Etiqueta los hablantes como 'A.T.' o 'C.' basado en las etiquetas originales.
Archivo de transcripción: Mantiene las etiquetas originales de los hablantes y elimina prefijos redundantes.

Flujo Principal del Script

Listado de Archivos de Audio

Crea una lista de rutas completas a todos los archivos MP3 en la carpeta de entrada.

Procesamiento en Paralelo

Utiliza multiprocessing.Pool() para crear un grupo de procesos.
Aplica la función transcribir_audio a cada archivo de audio en paralelo usando map().

Finalización: Cierra y espera a que todos los procesos terminen.


Notas Adicionales

El script está diseñado para manejar archivos MP3 específicamente.
Utiliza codificación UTF-8 para escribir los archivos de salida.
La transcripción incluye etiquetas de hablantes, que se modifican en el archivo de chat.

Rendimiento: El uso de multiprocessing permite un procesamiento eficiente de múltiples archivos en paralelo, aprovechando sistemas multi-núcleo.







################################### DESCRIPCION CODIGO AJUSTAR TRANSCRIPCION
## Descripción General
Este script de Python está diseñado para procesar archivos de texto en una carpeta específica, eliminando etiquetas de hablantes (como 'A:', 'B:', etc.) al inicio de cada línea o frase.
Importaciones

os: Para operaciones del sistema de archivos y manipulación de rutas.
re: Para realizar operaciones de expresiones regulares.

Funciones
eliminar_etiquetas(texto)
Esta función elimina las etiquetas de hablantes del texto proporcionado.
Parámetros:

texto: El texto a procesar.

Proceso:

Define un patrón de expresión regular que busca letras de A a I seguidas de dos puntos y un espacio al inicio de una palabra.
Utiliza re.sub() para reemplazar todas las ocurrencias del patrón con una cadena vacía.
Retorna el texto procesado.

procesar_archivo(ruta_archivo)
Esta función procesa un archivo individual, eliminando las etiquetas y sobrescribiendo el archivo original.
Parámetros:

ruta_archivo: La ruta completa al archivo a procesar.

Proceso:

Abre el archivo en modo lectura y lee todo su contenido.
Llama a eliminar_etiquetas() para procesar el contenido.
Imprime el contenido procesado (para fines de depuración o verificación).
Abre el mismo archivo en modo escritura y escribe el contenido procesado, sobrescribiendo el archivo original.

Flujo Principal del Script

Definición de la Carpeta

Establece la ruta a la carpeta que contiene los archivos a procesar.


Iteración sobre Archivos

Utiliza os.listdir() para obtener una lista de todos los archivos en la carpeta.
Para cada archivo:

Verifica si el archivo termina con '.txt'.
Si es así, construye la ruta completa al archivo.
Llama a procesar_archivo() con la ruta completa.

Notas Adicionales

El script está diseñado para trabajar con archivos de texto (.txt) específicamente.
Utiliza codificación UTF-8 para leer y escribir los archivos.
El script sobrescribe los archivos originales, por lo que no se mantiene una copia de respaldo.




################################### DESCRIPCION CODIGO ASISTENTE
## Descripción General
Este script de Python está diseñado para automatizar el proceso de calificación de llamadas en un centro de atención al cliente. Utiliza inteligencia artificial (IA) para analizar transcripciones de llamadas, asignar calificaciones basadas en guías predefinidas y almacenar los resultados en una base de datos MySQL.
Dependencias

os
mysql.connector
openai
json
time
sys
traceback

Configuración
Se requiere una clave API de OpenAI.
Conexión a una base de datos MySQL.
Estructura de carpetas específica para almacenar archivos de entrada y salida.

Funciones Principales
Funciones de Asistentes de IA

hacer_pregunta_assiis_servicios(pregunta)
hacer_pregunta_assiis_soporte(pregunta)
hacer_pregunta_assiis_retenciones(pregunta)

Estas funciones utilizan diferentes asistentes de OpenAI para analizar transcripciones de llamadas según el tipo de servicio (general, soporte, retenciones).

hacer_pregunta_min_tokens(fragmento_texto)
Utiliza el modelo GPT-4 para realizar análisis de calidad con un enfoque en minimizar el uso de tokens.

guia_set(guia, carpeta_archivos, carpeta_data)
Procesa archivos de transcripción según una guía específica, utilizando el asistente de IA apropiado para generar calificaciones.

extraccion(guia)
Extrae información de calificación de la base de datos y la convierte en un formato JSON.

extraccion_1() y extraccion_2()
Extraen datos JSON de archivos de texto y los guardan en archivos JSON separados.

eliminar_comillas_numeros_en_carpeta()
Limpia los archivos JSON, convirtiendo strings numéricos a enteros.

comparacion()
Compara y combina datos de dos conjuntos de archivos JSON.

eliminar_json()
Elimina el formato JSON de los archivos, dejando solo la tabla de calificaciones.

archivo_ya_subido(cursor, guia, file_name)
Verifica si un archivo ya ha sido subido a la base de datos.

cargar_calificaciones_en_mysql(guia)
Carga las calificaciones procesadas en la base de datos MySQL.

main()
Función principal que orquesta todo el proceso de calificación.

Flujo de Trabajo

Se selecciona una guía específica.
Se procesan las transcripciones de llamadas utilizando IA.
Se extraen y formatean los datos de calificación.
Se comparan y combinan los resultados.
Se cargan los resultados finales en la base de datos MySQL.

Uso
El script se ejecuta desde la línea de comandos, especificando la guía a utilizar:
Copypython nombre_del_script.py nombre_de_la_guia

Notas Importantes
El script depende de una estructura de carpetas específica y de la configuración correcta de la base de datos.
Se utilizan múltiples modelos de IA de OpenAI, cada uno especializado en diferentes aspectos del análisis de llamadas.
El proceso incluye varios pasos de extracción, transformación y carga de datos (ETL).
Se implementan verificaciones para evitar duplicados en la base de datos.






################################### DESCRIPCION CODIGO RESULTADOS CAL
# Documentación del Script de Carga de Resultados de Calificaciones

## ## Descripción General

Este script de Python está diseñado para procesar y cargar resultados de calificaciones en una base de datos MySQL. El script lee archivos de transcripción, obtiene valores de una tabla guía, calcula calificaciones basadas en ciertos criterios, y actualiza los resultados en la base de datos.

## Requisitos

- Python 3.x
- Biblioteca `mysql.connector`
- Acceso a una base de datos MySQL

## Funciones Principales

### 1. `obtener_valores(guia)`

Obtiene valores de una tabla guía en la base de datos.

- **Parámetros**: 
  - `guia`: Nombre de la tabla guía
- **Retorna**: Lista de tuplas con `id_subcategoria` y `nombre_punto`

### 2. `obtener_fila_por_nombre(guia, archivo)`

Obtiene los valores de calificación para un archivo específico.

- **Parámetros**:
  - `guia`: Nombre de la guía (usado para construir el nombre de la tabla)
  - `archivo`: Nombre del archivo de transcripción
- **Retorna**: Lista con los valores de calificación

### 3. `obtener_nombres_columnas(cursor, tabla)`

Obtiene los nombres de las columnas de una tabla específica.

- **Parámetros**:
  - `cursor`: Cursor de la conexión MySQL
  - `tabla`: Nombre de la tabla
- **Retorna**: Lista con los nombres de las columnas

### 4. `obtener_sumas(resultados_emparejados)`

Calcula sumas parciales de los resultados.

- **Parámetros**:
  - `resultados_emparejados`: Lista de resultados emparejados
- **Retorna**: Diccionario con sumas parciales

### 5. `imprimir_resultados_emparejados(resultados_emparejados)`

Calcula e imprime los resultados para guías específicas (set_1 o set_12).

- **Parámetros**:
  - `resultados_emparejados`: Lista de resultados emparejados
- **Retorna**: Suma total de calificaciones

### 6. `imprimir_resultados_emparejados_soporte(resultados_emparejados)`

Calcula e imprime los resultados para guías de soporte (set_9, set_10, o set_11).

- **Parámetros**:
  - `resultados_emparejados`: Lista de resultados emparejados
- **Retorna**: Suma total de calificaciones

### 7. `actualizar_resultado(resultado, valor_columna, guia)`

Actualiza el resultado de la calificación en la base de datos.

- **Parámetros**:
  - `resultado`: Valor de la calificación
  - `valor_columna`: Nombre del archivo (usado como identificador)
  - `guia`: Nombre de la guía

### 8. `main(guia)`

Función principal que coordina todo el proceso.

- **Parámetros**:
  - `guia`: Nombre de la guía a procesar

## Flujo de Ejecución

1. El script comienza imprimiendo un mensaje de inicio.
2. Se obtienen los valores de la tabla guía especificada.
3. Se procesan los archivos de transcripción en la carpeta especificada.
4. Para cada archivo:
   - Se obtienen los valores de calificación de la base de datos.
   - Se emparejan los resultados con los valores de la guía.
   - Se calculan las calificaciones según el tipo de guía.
   - Se actualiza el resultado en la base de datos.
5. Se imprime la suma total de calificaciones.

## Uso

El script puede ser ejecutado desde la línea de comandos, proporcionando el nombre de la guía como argumento:

```
python nombre_del_script.py nombre_de_la_guia
```

Alternativamente, se puede modificar el script para uso manual descomentando y ajustando las últimas líneas del código.

## Notas Adicionales

- El script utiliza una conexión a una base de datos MySQL local (host: '192.168.51.210').
- Los archivos de transcripción deben estar en la carpeta 'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'.
- El script maneja diferentes lógicas de cálculo para distintos tipos de guías (servicios/retenciones vs. soporte).





################################### DESCRIPCION CODIGO JUSTIFICACION PENALIZACION Y MARIANA
# Documentación del Script de Extracción y Carga de Penalizaciones

## Descripción General

Este script de Python está diseñado para procesar archivos de texto que contienen información sobre penalizaciones, extraer datos relevantes, y cargarlos en una base de datos MySQL. El script categoriza las penalizaciones, las agrupa por categorías predefinidas, y las inserta en una tabla de base de datos específica.

## Componentes Principales

### 1. Diccionarios y Conjuntos de Parámetros

- `parametros_categorias`: Un diccionario que mapea parámetros específicos a categorías más amplias.
- `parametros_categorias_base`: Un conjunto que define las categorías base utilizadas en la base de datos.

### 2. Funciones Principales

#### `extract_data_from_file(file_path)`

Esta función extrae datos de un archivo de texto y los organiza en categorías.

- **Parámetros**: 
  - `file_path`: Ruta al archivo de texto a procesar
- **Retorna**: Un diccionario donde las claves son categorías y los valores son listas de penalizaciones formateadas.

#### `main(guia, tipo)`

La función principal que coordina todo el proceso de extracción y carga de datos.

- **Parámetros**:
  - `guia`: Nombre de la guía
  - `tipo`: Tipo de datos (no se especifica su uso en el código proporcionado)

## Flujo de Ejecución

1. El script se inicia con dos argumentos de línea de comandos: `guia` y `tipo`.
2. Se establece una conexión a la base de datos MySQL.
3. Se define la ruta de la carpeta que contiene los archivos de texto a procesar.
4. Para cada archivo en la carpeta:
   - Se extrae la información de penalizaciones usando `extract_data_from_file()`.
   - Se formatea la información extraída en una tupla de datos.
   - Se agrega la tupla a una lista de datos a insertar.
5. Se prepara una consulta SQL para insertar los datos en la tabla `justificacion_penalizaciones_guias`.
6. Se ejecuta la inserción de datos en lote (bulk insert) usando `executemany()`.
7. Se confirman (commit) los cambios en la base de datos.
8. Se cierran la conexión y el cursor de la base de datos.

## Detalles de Implementación

### Extracción de Datos
- Utiliza expresiones regulares para extraer información de los archivos de texto.
- Agrupa las penalizaciones por categorías definidas en `parametros_categorias`.

### Formateo de Datos
- Crea una tupla de datos para cada archivo, incluyendo el nombre del archivo, las penalizaciones por categoría, y metadatos adicionales.
- Maneja casos donde no hay penalizaciones para una categoría específica.

### Inserción en la Base de Datos
- Utiliza una inserción parametrizada para prevenir inyecciones SQL.
- Realiza una inserción en lote para mejorar la eficiencia.

## Uso

El script se ejecuta desde la línea de comandos con dos argumentos:

```
python nombre_del_script.py guia tipo
```

Donde:
- `guia` es el nombre de la guía que se está procesando.
- `tipo` es un parámetro adicional (su uso específico no está claro en el código proporcionado).

## Notas Adicionales

- El script asume una estructura específica en los archivos de texto de entrada.
- La conexión a la base de datos se realiza a un servidor local (192.168.51.210) sin contraseña, lo cual puede representar un riesgo de seguridad en un entorno de producción.
- El script no maneja excepciones, lo que podría llevar a errores no controlados en caso de problemas con los archivos o la conexión a la base de datos.








################################### DESCRIPCION CODIGO EMOCIONES
Este script en Python analiza el sentimiento de transcripciones de texto almacenadas en archivos y las clasifica en emociones positivas, neutrales o negativas utilizando la herramienta VADER de NLTK. A continuación, te explico en detalle cada sección del código:

1. Importación de bibliotecas
python
Copiar código
import os
import glob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
Se importan las bibliotecas necesarias:

os: Permite interactuar con el sistema de archivos.
glob: Para obtener rutas de archivos que coincidan con un patrón específico.
nltk: Biblioteca de lenguaje natural que incluye el analizador de sentimientos.
SentimentIntensityAnalyzer: Parte de la librería VADER de NLTK, utilizada para el análisis de sentimiento.
2. Función principal emociones_dato()
Esta es la función central que realiza el procesamiento de archivos de texto para obtener emociones.

2.1. Descargar el lexicón VADER
python
Copiar código
nltk.download('vader_lexicon')
El código descarga el conjunto de datos necesarios para el análisis de sentimientos de VADER.

2.2. Función para leer el contenido de los archivos
python
Copiar código
def transcribe_text(text_path):
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
Esta función abre un archivo de texto y devuelve su contenido en forma de cadena.

2.3. Configuración de carpetas y archivos
python
Copiar código
folder_path = r'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'
results_folder = r'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\emociones'
os.makedirs(results_folder, exist_ok=True)
text_paths = glob.glob(folder_path + '/*.txt')
Se definen las rutas de carpetas para los archivos de entrada y de salida. Los archivos de texto que serán procesados se buscan en la carpeta de transcripciones usando glob. Los resultados se guardan en una carpeta de emociones, la cual se crea si no existe.

2.4. Inicialización del analizador de sentimientos
python
Copiar código
sia = SentimentIntensityAnalyzer()
Se instancia el objeto de SentimentIntensityAnalyzer, que será utilizado para obtener las puntuaciones de sentimiento de los textos.

2.5. Procesamiento de archivos
python
Copiar código
for text_path in text_paths:
    file_name = os.path.splitext(os.path.basename(text_path))[0]
    result_file = os.path.join(results_folder, file_name + '.txt')
Se itera sobre cada archivo de texto, extrayendo el nombre del archivo sin la extensión. Se verifica si ya ha sido procesado antes; si es así, se omite.

2.6. División del texto en secciones
python
Copiar código
secciones = descomponer_prompt(text, 4090)
Dado que el analizador de sentimientos puede tener un límite en la longitud del texto, este se divide en secciones de un tamaño manejable utilizando la función descomponer_prompt().

2.7. Cálculo de sentimientos
python
Copiar código
scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
for seccion in secciones:
    sentiment_scores = sia.polarity_scores(seccion)
    scores['neg'] += sentiment_scores['neg']
    scores['neu'] += sentiment_scores['neu']
    scores['pos'] += sentiment_scores['pos']
    scores['compound'] += sentiment_scores['compound']
Para cada sección, se obtienen las puntuaciones de negatividad, neutralidad, positividad y el sentimiento compuesto (una medida general de sentimiento). Luego, estas puntuaciones se suman.

2.8. Promediado de sentimientos
python
Copiar código
num_secciones = len(secciones)
scores['neg'] /= num_secciones
scores['neu'] /= num_secciones
scores['pos'] /= num_secciones
scores['compound'] /= num_secciones
Después de procesar todas las secciones, se dividen los puntajes por la cantidad de secciones para obtener los promedios.

2.9. Determinación de la emoción predominante
python
Copiar código
max_emotion = max(scores['neg'], scores['neu'], scores['pos'])
scores['neg'] = 1 if scores['neg'] == max_emotion else 0
scores['neu'] = 1 if scores['neu'] == max_emotion else 0
scores['pos'] = 1 if scores['pos'] == max_emotion else 0
Se compara qué emoción (negativa, neutral o positiva) tiene el puntaje más alto y se establece como dominante, asignando un valor de 1 a la emoción más fuerte y 0 a las demás.

2.10. Impresión y guardado de resultados
python
Copiar código
with open(result_file, 'w') as file:
    file.write(f"Análisis de sentimientos del archivo de texto: {file_name}\n")
    file.write(f"Puntuación de negatividad: {scores['neg']}\n")
    file.write(f"Puntuación de neutralidad: {scores['neu']}\n")
    file.write(f"Puntuación de positividad: {scores['pos']}\n")
    file.write(f"Puntuación de sentimiento general: {scores['compound']}\n")
El código imprime los resultados y también guarda las puntuaciones de cada archivo en un nuevo archivo de texto.

3. Función auxiliar descomponer_prompt()
python
Copiar código
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
Esta función divide un texto largo en partes más pequeñas, buscando un punto adecuado (usualmente un punto final). Si no encuentra un punto, simplemente corta el texto en el límite máximo.

4. Bloque principal
python
Copiar código
if __name__ == "__main__":
    emociones_dato()
    print("\n--------- FINALIZA OBTENCION DE EMOCIONES CON EXITO ---------\n")
Finalmente, este bloque asegura que cuando se ejecute el script directamente, se llame a la función principal para iniciar el análisis.

En resumen, este código se encarga de analizar el sentimiento de múltiples archivos de texto, descomponiendo los textos largos si es necesario, calculando las emociones dominantes, y luego guardando los resultados en archivos separados.







################################### DESCRIPCION CODIGO EXTRACCION DE RESULTADOS

Este código en Python tiene como objetivo procesar varios archivos de texto que se encuentran en una carpeta específica. Extrae información clave de estos archivos utilizando expresiones regulares y luego guarda los resultados en diferentes carpetas, dependiendo del tipo de información extraída. A continuación, se detalla la funcionalidad de cada parte del código:

1. Importación de bibliotecas
python
Copiar código
import os
import re
os: Se utiliza para interactuar con el sistema de archivos (crear directorios, listar archivos, etc.).
re: Se emplea para trabajar con expresiones regulares, que se usan para extraer información específica de los archivos de texto.
2. Definición de rutas
python
Copiar código
ruta_principal = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\calificacion\pov1"
ruta_resumen = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\resumen"
ruta_reincidencias = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\reincidencia"
ruta_insatisfacciones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\insatisfaccion"
ruta_emociones = r"C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones"
Estas son las rutas donde se almacenan los archivos de texto que se procesarán, así como las carpetas donde se guardarán los resultados:

ruta_principal: Carpeta donde están los archivos originales de texto.
ruta_resumen: Carpeta donde se guardarán los resúmenes extraídos de los archivos.
ruta_reincidencias: Carpeta para guardar las reincidencias extraídas.
ruta_insatisfacciones: Carpeta donde se almacenarán las insatisfacciones.
ruta_emociones: Carpeta para las justificaciones emocionales extraídas.
3. Creación de carpetas si no existen
python
Copiar código
os.makedirs(ruta_resumen, exist_ok=True)
os.makedirs(ruta_reincidencias, exist_ok=True)
os.makedirs(ruta_insatisfacciones, exist_ok=True)
os.makedirs(ruta_emociones, exist_ok=True)
Se crean las carpetas para almacenar los resultados si aún no existen. El parámetro exist_ok=True asegura que no se lance una excepción si las carpetas ya están creadas.

4. Función extraer_informacion_contenido(contenido)
python
Copiar código
def extraer_informacion_contenido(contenido):
    resumen = re.search(r'Resumen:\n(.*?)\nReincidencia:', contenido, re.DOTALL)
    reincidencia = re.search(r'Reincidencia:\s*(\d+)', contenido)
    insatisfaccion = re.search(r'Insatisfacción:\s*(\d+)', contenido)
    emocion = re.search(r'Explicación emocional:\s*(.*)', contenido)

    return {
        "resumen": resumen.group(1).strip() if resumen else "",
        "reincidencia": reincidencia.group(1).strip() if reincidencia else "",
        "insatisfaccion": insatisfaccion.group(1).strip() if insatisfaccion else "",
        "emocion": emocion.group(1).strip() if emocion else ""
    }
Esta función toma el contenido de un archivo de texto como argumento y utiliza expresiones regulares para extraer cuatro tipos de información:

Resumen: Busca el texto entre la palabra clave "Resumen:" y "Reincidencia:".
Reincidencia: Busca un número que aparece después de la palabra "Reincidencia:".
Insatisfacción: Busca un número que aparece después de "Insatisfacción:".
Emoción: Busca el texto que sigue después de "Explicación emocional:".
La función devuelve un diccionario con los valores extraídos. Si no se encuentra la información esperada, la función devuelve una cadena vacía para esa clave.

5. Función guardar_datos(nombre_archivo, datos)
python
Copiar código
def guardar_datos(nombre_archivo, datos):
    with open(os.path.join(ruta_resumen, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["resumen"])

    with open(os.path.join(ruta_reincidencias, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["reincidencia"])

    with open(os.path.join(ruta_insatisfacciones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["insatisfaccion"])

    with open(os.path.join(ruta_emociones, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(datos["emocion"])
Esta función toma el nombre del archivo original y el diccionario con los datos extraídos. Luego, guarda cada parte de la información en su respectiva carpeta:

Resumen: Guardado en la carpeta de resúmenes.
Reincidencia: Guardado en la carpeta de reincidencias.
Insatisfacción: Guardado en la carpeta de insatisfacciones.
Emoción: Guardado en la carpeta de emociones.
Cada archivo se guarda con el mismo nombre que el archivo original, pero en la carpeta correspondiente y con el contenido adecuado.

6. Iteración sobre los archivos en la carpeta principal
python
Copiar código
for archivo in os.listdir(ruta_principal):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(ruta_principal, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        datos_extraidos = extraer_informacion_contenido(contenido)
        guardar_datos(archivo, datos_extraidos)
Este bloque de código realiza las siguientes acciones:

Listar archivos: Se listan todos los archivos en la carpeta ruta_principal.
Filtrar archivos de texto: Se procesan únicamente los archivos que tienen la extensión .txt.
Leer contenido del archivo: Se abre cada archivo y se lee todo su contenido en una cadena.
Extraer información: Se llama a la función extraer_informacion_contenido() para obtener el resumen, reincidencia, insatisfacción y emoción del contenido.
Guardar resultados: Se llama a la función guardar_datos() para almacenar cada parte de la información en su carpeta correspondiente.
7. Mensaje final
python
Copiar código
print("Análisis completado.")
Finalmente, se imprime un mensaje en la consola indicando que el proceso de análisis ha sido completado.

Resumen
Este script automatiza el procesamiento de múltiples archivos de texto, extrayendo información clave como resúmenes, reincidencias, niveles de insatisfacción y justificaciones emocionales. Luego, organiza estos datos en carpetas separadas para facilitar su revisión o análisis posterior. Utiliza expresiones regulares para identificar y extraer las secciones relevantes del contenido de cada archivo de texto.






################################### DESCRIPCION CODIGO INSERCION DATOS FALTANTES

## Descripción General

Este script en Python está diseñado para automatizar la actualización de ciertas columnas en una base de datos MySQL (`audios_dana`) a partir de archivos de texto almacenados en carpetas específicas en el sistema de archivos local. El script se conecta a la base de datos, selecciona registros que requieren actualización (donde las columnas específicas están `NULL` o vacías), lee el contenido de los archivos correspondientes y actualiza las columnas en la base de datos con estos datos.

## Requisitos

- **Python 3.x**: Asegúrate de tener una versión de Python 3 instalada.
- **Bibliotecas Python**:
  - `mysql-connector-python`: Para conectar y ejecutar consultas en MySQL.
  - `os`: Para manejar rutas y operaciones del sistema de archivos.

## Instalación de Dependencias

Puedes instalar la biblioteca necesaria utilizando `pip`:

```bash
pip install mysql-connector-python
```

## Configuración de la Base de Datos

El script utiliza una configuración de conexión a la base de datos definida en cada función:

```python
db_config = {
    'host': '192.168.51.210',
    'user': 'root',
    'password': 'thor',
    'database': 'audios_dana'
}
```

- **host**: Dirección IP del servidor de la base de datos.
- **user**: Nombre de usuario para acceder a la base de datos.
- **password**: Contraseña del usuario (actualmente está vacía).
- **database**: Nombre de la base de datos a utilizar.

*Asegúrate de que estos parámetros coincidan con tu configuración de base de datos.*

## Estructura del Código

El script contiene varias funciones, cada una encargada de actualizar una columna específica en la base de datos a partir de archivos de texto:

### 1. `transcripciones()`

**Descripción**: Actualiza la columna `transcripcion` en la tabla `prueba_dana_calidad`.

**Proceso**:
- Conecta a la base de datos.
- Selecciona hasta 30 registros donde `transcripcion` está `NULL` o vacía.
- Para cada registro:
  - Obtiene el nombre del archivo correspondiente en la carpeta `transcripciones`.
  - Si el archivo existe, lee su contenido.
  - Actualiza la columna `transcripcion` con el contenido del archivo.
  - Confirma la transacción en la base de datos.
  - Imprime un mensaje de éxito o de archivo no encontrado.

### 2. `chat()`

**Descripción**: Actualiza la columna `chat` en la tabla `prueba_dana_calidad`.

**Proceso**:
- Similar a `transcripciones()`, pero trabaja con la columna `chat` y la carpeta `chat`.
- Lee archivos de texto desde `C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\chat`.

### 3. `transcripcion_original()`

**Descripción**: Actualiza la columna `transcripcion_original` en la tabla `prueba_dana_calidad`.

**Proceso**:
- Similar a `transcripciones()`, pero trabaja con la columna `transcripcion_original`.
- Lee archivos de texto desde `C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones`.

### 4. `justificacion_emociones()`

**Descripción**: Actualiza la columna `justificacion_emociones` en la tabla `prueba_dana_calidad`.

**Proceso**:
- Similar a las funciones anteriores, pero trabaja con la columna `justificacion_emociones`.
- Lee archivos de texto desde `C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones`.
- **Nota**: Utiliza codificación `latin-1` al leer los archivos.

### 5. `resumen()`

**Descripción**: Actualiza la columna `resumen` en la tabla `contextos_calidad`.

**Proceso**:
- Similar a las funciones anteriores, pero trabaja con la columna `resumen` en una tabla diferente (`contextos_calidad`).
- Lee archivos de texto desde `C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\justificacion_emociones`.
- **Nota**: Utiliza codificación `latin-1` al leer los archivos.

## Uso del Script

El script está diseñado para ejecutarse directamente. Al ejecutar el archivo Python, se ejecutarán todas las funciones de actualización en el siguiente orden:

1. `transcripciones()`
2. `chat()`
3. `transcripcion_original()`
4. `justificacion_emociones()`
5. `resumen()`

### Ejecución

Desde la línea de comandos, navega al directorio que contiene el script y ejecuta:

```bash
python nombre_del_script.py
```

*Asegúrate de reemplazar `nombre_del_script.py` con el nombre real del archivo.*

## Detalles Técnicos

### Conexión a la Base de Datos

Cada función establece una nueva conexión a la base de datos utilizando los parámetros definidos en `db_config`. Después de completar las operaciones, cierra tanto el cursor como la conexión para liberar recursos.

### Manejo de Archivos

- **Ruta de las carpetas**: Las rutas de las carpetas están definidas de forma absoluta. Si cambian las ubicaciones de los archivos, actualiza las rutas correspondientes en cada función.
- **Codificación**:
  - Generalmente, los archivos se leen con `utf-8`.
  - En `justificacion_emociones()` y `resumen()`, se utiliza `latin-1` debido a posibles caracteres especiales presentes en estos archivos.

### Consultas SQL

- **Selección de registros**: Utiliza una consulta `SELECT` con condiciones para seleccionar registros donde la columna específica es `NULL` o está vacía. Ordena los resultados en orden descendente por `id_audio` y limita la selección a 30 registros.
  
  ```sql
  SELECT id_audio, filename 
  FROM prueba_dana_calidad 
  WHERE columna_especifica IS NULL OR columna_especifica = ''
  ORDER BY id_audio DESC LIMIT 30;
  ```

- **Actualización de registros**: Utiliza una consulta `UPDATE` para establecer el valor de la columna específica con el contenido leído del archivo.

  ```sql
  UPDATE prueba_dana_calidad 
  SET columna_especifica = %s 
  WHERE id_audio = %s;
  ```

### Manejo de Errores

El script imprime mensajes en la consola para indicar el éxito de las actualizaciones o si un archivo no se encontró. No implementa manejo de excepciones más allá de esto, por lo que es recomendable agregar manejo de errores para escenarios como fallos en la conexión a la base de datos o errores al leer archivos.

## Mejoras Sugeridas

- **Manejo de Excepciones**: Implementar bloques `try-except` para capturar y manejar posibles errores durante la conexión a la base de datos, la ejecución de consultas o la lectura de archivos.
- **Configuración Externa**: Externalizar la configuración de la base de datos y las rutas de las carpetas en un archivo de configuración (por ejemplo, `config.json` o variables de entorno) para facilitar su mantenimiento y seguridad.
- **Logging**: Utilizar la biblioteca `logging` de Python para registrar eventos en lugar de imprimir directamente en la consola. Esto permite un mejor seguimiento y depuración.
- **Optimización de Consultas**: Revisar la lógica de selección de registros para evitar actualizaciones innecesarias y mejorar el rendimiento si el volumen de datos es grande.
- **Interfaz de Usuario**: Crear una interfaz (por ejemplo, línea de comandos con opciones) para seleccionar qué actualizaciones ejecutar, en lugar de ejecutarlas todas automáticamente.

## Conclusión

Este script automatiza la actualización de varias columnas en una base de datos MySQL a partir de archivos de texto locales. Es una herramienta útil para mantener la integridad y completitud de los datos en la base de datos, asegurando que las transcripciones, chats y otros campos importantes estén siempre actualizados con la información correspondiente.








################################### DESCRIPCION CODIGO COMPLETADO

## Descripción General

Este código en Python tiene como objetivo actualizar el estado de los registros de audios en una base de datos MySQL. La función principal (`status_completado`) busca archivos de transcripción en una carpeta específica en el sistema local. Si el nombre de un archivo de transcripción coincide con un registro en la base de datos y su estado no es "Audio de baja calidad", el registro es actualizado con un estado de "Completado" y marcado como analizado.

## Requisitos

- **Python 3.x**: Necesitas una versión de Python 3 instalada en tu sistema.
- **Bibliotecas Python**:
  - `mysql-connector-python`: Para conectar y ejecutar consultas en MySQL.
  - `os`: Para manejar rutas y operaciones del sistema de archivos.

## Instalación de Dependencias

Puedes instalar la biblioteca necesaria utilizando `pip`:

```bash
pip install mysql-connector-python
```

## Configuración de la Base de Datos

El código se conecta a una base de datos MySQL con la siguiente configuración:

```python
conexion = mysql.connector.connect(
    host="192.168.51.210",
    user="root",
    password="thor",
    database="audios_dana"
)
```

- **host**: Dirección IP del servidor de la base de datos.
- **user**: Nombre de usuario para acceder a la base de datos.
- **password**: Contraseña del usuario (vacía en este caso).
- **database**: Nombre de la base de datos (`audios_dana`).

*Asegúrate de modificar estos parámetros según tu configuración de base de datos.*

## Proceso del Código

### 1. Conexión a la Base de Datos

La función comienza estableciendo una conexión con la base de datos `audios_dana` y creando un cursor para ejecutar las consultas.

### 2. Obtención de los Registros de la Base de Datos

El siguiente paso es ejecutar una consulta SQL que selecciona los nombres de archivo de audio (`audio_name`) y el estado (`status`) de todos los registros en la tabla `audios`.

```python
cursor.execute("SELECT audio_name, status FROM audios")
registros_audios = cursor.fetchall()
```

El resultado se guarda en la variable `registros_audios`, que es una lista de tuplas. Después, se crea un diccionario `nombres_archivo_existente` donde la clave es el nombre del archivo de audio y el valor es su estado actual.

### 3. Lectura de Archivos en la Carpeta de Transcripciones

El código procede a leer los archivos de transcripción almacenados en la carpeta especificada:

```python
carpeta_transcripcion = r'C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones'
```

Para cada archivo en la carpeta de transcripciones, se extrae el nombre sin la extensión y se le agrega la extensión `.mp3` para compararlo con los nombres de audio almacenados en la base de datos.

### 4. Actualización de la Base de Datos

Si el nombre del archivo de audio existe en la base de datos y su estado no es "Audio de baja calidad", se actualiza el registro con los siguientes valores:

- `analyzed = 1`: Indica que el audio ha sido analizado.
- `status = 'Completado'`: Establece el estado del audio como "Completado".
- `analizado_tareas = 1`: Marca que el audio ha sido analizado en otras tareas.

La consulta de actualización es:

```python
consulta = "UPDATE audios SET analyzed = 1, status = 'Completado', analizado_tareas = 1 WHERE audio_name = %s"
cursor.execute(consulta, (nombre_archivo,))
```

### 5. Confirmación de Cambios y Cierre de Conexiones

Una vez que se han realizado todas las actualizaciones, los cambios se confirman con `conexion.commit()`. Finalmente, el cursor y la conexión a la base de datos se cierran para liberar recursos.

```python
conexion.commit()
cursor.close()
conexion.close()
```

## Uso del Script

Este script está diseñado para ejecutarse directamente desde la línea de comandos. Al ejecutarlo, buscará en la carpeta de transcripciones y actualizará los registros correspondientes en la base de datos.

### Ejecución

Para ejecutar el script, utiliza la siguiente línea de comando:

```bash
python nombre_del_script.py
```

Asegúrate de reemplazar `nombre_del_script.py` por el nombre real del archivo.

## Detalles Técnicos

### Conexión a la Base de Datos

El código utiliza `mysql.connector` para conectarse a la base de datos MySQL y realizar las consultas necesarias. La conexión se cierra al finalizar la ejecución.

### Lectura de Archivos en la Carpeta

El módulo `os` se utiliza para listar todos los archivos dentro de la carpeta `C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones`. La función `os.listdir()` devuelve una lista de archivos en la carpeta, y `os.path.splitext()` se utiliza para obtener el nombre del archivo sin la extensión.

### Condicional de Estado

Antes de actualizar un registro en la base de datos, se verifica que el estado del audio no sea "Audio de baja calidad":

```python
if estado_actual != 'Audio de baja calidad':
```

Esta condición evita que se actualicen los registros de audios que ya han sido marcados como de baja calidad.

### Actualización de Registros

La actualización en la base de datos se realiza a través de una consulta `UPDATE`, que se ejecuta solo si el nombre del archivo coincide con un registro en la base de datos y cumple la condición mencionada.

## Mejoras Sugeridas

- **Manejo de Excepciones**: Agregar bloques `try-except` para manejar posibles errores durante la conexión a la base de datos o la manipulación de archivos.
- **Logging**: Utilizar la biblioteca `logging` para registrar las actualizaciones realizadas, los errores o advertencias, y evitar depender únicamente de `print()`.
- **Parámetros Configurables**: Externalizar la configuración de la conexión a la base de datos y la ruta de la carpeta en un archivo de configuración para una mayor flexibilidad.
- **Procesamiento en Lote**: En caso de grandes volúmenes de datos, se podría optimizar el proceso dividiendo los registros en lotes más pequeños y procesarlos en paralelo.
  
## Conclusión

Este script automatiza el proceso de verificar archivos de transcripción y actualizar los estados correspondientes en la base de datos. Es útil para asegurar que los audios que han sido procesados tengan su estado actualizado correctamente en el sistema.





################################### DESCRIPCION CODIGO ELIMINAR DATOS
# Documentación del Código

## Descripción General

Este script en Python está diseñado para eliminar todos los archivos de múltiples carpetas especificadas. Es útil para tareas de limpieza donde se necesita vaciar directorios específicos de archivos, como en un proceso de eliminación masiva de archivos temporales o de trabajo.

## Requisitos

- **Python 3.x**: El script requiere una versión de Python 3 para funcionar correctamente.
- **Biblioteca `os`**: La biblioteca `os` de Python se utiliza para interactuar con el sistema de archivos, permitiendo listar archivos, unir rutas y eliminar archivos.

## Funciones del Script

### 1. `eliminar_archivos_en_carpetas(carpetas)`

Esta función recibe una lista de carpetas como argumento y elimina todos los archivos que se encuentran dentro de ellas.

#### Flujo de la función:

1. **Iterar sobre las carpetas**: Para cada carpeta en la lista de carpetas proporcionada, se listan todos los archivos usando `os.listdir()`.
   
2. **Construir la ruta completa**: La función `os.path.join()` se usa para crear la ruta completa de cada archivo dentro de la carpeta.

3. **Comprobar si es un archivo**: Utiliza `os.path.isfile()` para asegurarse de que el elemento en cuestión es un archivo (y no un directorio u otro tipo de objeto).

4. **Eliminar archivos**: Si es un archivo, se intenta eliminar con `os.remove()`. En caso de éxito, imprime un mensaje indicando que el archivo fue eliminado. Si ocurre un error (como permisos insuficientes o archivos bloqueados), se captura la excepción y se imprime un mensaje de error.

### 2. `elim()`

Esta función es una lista de rutas a las carpetas que se desean vaciar. Llama a la función `eliminar_archivos_en_carpetas()` con la lista de carpetas predefinidas.

Las carpetas incluyen:

- **C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\audios**
- **C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\chat**
- **C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\transcripciones**

...y varias otras relacionadas con procesos de transcripción, chat, emociones, y más.

### 3. Flujo Principal

El script imprime un mensaje de inicio y luego llama a la función `elim()` para eliminar archivos de todas las carpetas especificadas. Una vez que termina el proceso, imprime un mensaje de finalización exitosa.

#### Estructura:

```python
if __name__ == "__main__":
    print("\n--------- INICIANDO ELIMINACION DE ARCHIVOS ALMACENADOS ---------\n")
    elim()
    print("\n--------- FINALIZA ELIMINACION CON EXITO ---------\n")
```

## Uso

Este script está diseñado para ejecutarse directamente desde la línea de comandos. Simplemente puedes ejecutarlo para vaciar las carpetas especificadas de archivos.

### Ejecución

Para ejecutar el script, utiliza el siguiente comando:

```bash
python nombre_del_script.py
```

Donde `nombre_del_script.py` es el nombre del archivo en el que has guardado el código.

### Consideraciones

- **Carpetas Válidas**: Asegúrate de que las carpetas especificadas existan y que el usuario que ejecuta el script tenga permisos de lectura/escritura en esas ubicaciones.
- **Archivos no eliminados**: Si un archivo no se puede eliminar (por ejemplo, debido a permisos o si está en uso), se mostrará un mensaje de error indicando el archivo específico y la causa del error.

### Ejemplo de Salida:

```
--------- INICIANDO ELIMINACION DE ARCHIVOS ALMACENADOS ---------

Se ha eliminado el archivo: C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\audios\archivo1.txt
Se ha eliminado el archivo: C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\audios\archivo2.txt
No se pudo eliminar C:\Users\Jotzi1\Desktop\copias\Analisis_Masivo_guia\Proceso_Clidad_1\audios_extraidos\archivo3.txt: [Error de Permiso]

--------- FINALIZA ELIMINACION CON EXITO ---------
```

## Posibles Mejoras

- **Manejo de Excepciones Mejorado**: Se puede mejorar el manejo de errores para capturar y registrar más detalles sobre el tipo de error que ocurrió.
- **Validación de Carpetas**: Se puede añadir una validación previa para verificar si las carpetas existen antes de intentar acceder a ellas.
- **Logs**: Podrías utilizar el módulo `logging` de Python en lugar de `print()` para guardar un registro detallado de las operaciones.
- **Eliminar Carpetas Vacías**: Se puede añadir una función para eliminar también las carpetas si quedan vacías después de eliminar los archivos.

## Conclusión

Este script proporciona una manera eficiente y automatizada de eliminar archivos de múltiples carpetas en un solo proceso, ideal para limpiar grandes volúmenes de archivos en directorios específicos.