import requests
import json
import pandas as pd
import datetime
import sys, os
import csv
import pandas as pandasForSortingCSV
import time
from datetime import timezone

lista=[]
listaevento=[]

# URL base del servicio apara API
BASE_URL_EMSC = "http://www.seismicportal.eu/fdsnws/event/1/query?"
#BASE_URL_EMSC = "https://www.seismicportal.eu/fdsnws/event/1/query"
BASE_URL_USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
BASE_URL_GFZ = "http://geofon.gfz.de/fdsnws/event/1/query?"

"""
parametros para seleccionar el cuadrante para la sismicidad en chile
latitud: -70 a -17.5
longitud -113 a -50
"""
# parametros que vienen al ejecutar el script
starttime=sys.argv[1]
endtime=sys.argv[2]
minmag=sys.argv[3]
#maxmag=sys.argv[4]

parametros_EMSC = {
    'starttime': starttime,
    'endtime': endtime,
    'minmag': minmag,
    'minlatitude': -70,
    'maxlatitude' : -17.5,
    'minlongitude' : -113,
    'maxlongitude' : -50,
    'format': 'json'  # Solicitamos el formato JSON
}

parametros_USGS = {
    'starttime': starttime[:10],
    'endtime': endtime[:10],
    'minmag': minmag,
    'minlatitude': -70,
    'maxlatitude' : -17.5,
    'minlongitude' : -113,
    'maxlongitude' : -50,
    'format': 'geojson'  # Solicitamos el formato JSON
}

parametros_GFZ = {
    #'starttime': '2024-09-01',
    'starttime': starttime[:10],
    #'endtime': '2025-10-26',
    'endtime': endtime[:10],
    'minmag': minmag,
    'minlatitude': -70,
    'maxlatitude' : -17.5,
    'minlongitude' : -113,
    'maxlongitude' : -50,
    'format': 'text'  # En este caso es text
}

try:
    # 'requests.get' envía la solicitud. La librería se encarga de formatear la URL
    # correctamente con los parámetros que proporcionamos en cada diccionario.
    response_EMSC = requests.get(BASE_URL_EMSC, params=parametros_EMSC)
    response_USGS = requests.get(BASE_URL_USGS, params=parametros_USGS)
    
    # lanza una excepción para códigos de estado de error (4xx o 5xx)
    response_EMSC.raise_for_status()
    response_USGS.raise_for_status()

    # procesar la respuesta JSON
    # 'response.json()' convierte la respuesta de texto JSON a un diccionario de Python.
    datos_EMSC = response_EMSC.json()
    datos_USGS = response_USGS.json()

    # Los datos de los eventos sísmicos se encuentran dentro de 'features' solo para EMSC y USGS
    eventos_EMSC = datos_EMSC.get('features', [])
    eventos_USGS = datos_USGS.get('features', [])

    print(f"Solicitud exitosa, eventos encontrados en EMSC {len(eventos_EMSC)}")
    print(f"Solicitud exitosa, eventos encontrados en USGS {len(eventos_USGS)}")
        
    # procesa los datos obtenidos con la consulta a la API del EMSC
    if eventos_EMSC:
        for i, evento in enumerate(eventos_EMSC, 1):
            # La información principal del evento está en 'properties'
            propiedades = evento['properties']
            
            # Formatear la hora de origen (está en milisegundos Unix)
            # EMSC a menudo usa milisegundos, aunque el estándar FDSN es segundos.
            # Aquí se asume que el formato estándar FDSN-Event donde 'time' es un string ISO 8601.
            
            # parametroas del evento obtenidos tras la consulta
            fecha_hora = propiedades.get('time')
            lat = round(propiedades.get('lat'),3)
            lon = round(propiedades.get('lon'),3)
            profundidad = propiedades.get('depth')
            magnitud = propiedades.get('mag')
            tipomag = propiedades.get('magtype')
            lugar = propiedades.get('flynn_region', 'Región Desconocida')
            agencia_fuente = propiedades.get('auth')

            fecha_hora_limpia = fecha_hora.replace('Z', '')
            fechahora = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S.%f")
            fechahora_str = fechahora.strftime("%Y-%m-%d  %H:%M:%S")

            lista=fechahora_str, lat, lon, profundidad, magnitud, tipomag, lugar, agencia_fuente
            listaevento.append(lista)

        # Crea y nombra el DataFrame
        df_EMSC = pd.DataFrame(listaevento)
        df_EMSC.columns = ['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']

        # convierte a DATETIME y ordena
        df_EMSC['Fecha_Hora'] = pd.to_datetime(df_EMSC['Fecha_Hora'])
        df_EMSC = df_EMSC.sort_values(by='Fecha_Hora', ascending=True) 

        # resetear el índice
        # 'drop=False' mantiene el índice anterior como una nueva columna (que no usaremos).
        # 'inplace=True' modifica el DataFrame directamente.
        df_EMSC.reset_index(drop=True, inplace=True) 

        # crea el archivo .csv
        salida = 'consultaapi_EMSC.csv'
        df_EMSC.to_csv(salida, index=True)
        
    else:
        print("No se encontraron eventos sísmicos que coincidan con los criterios de búsqueda en el EMSC.")

    # procesa los datos obtenidos con la consulta a la API del USGS
    lista=[]
    listaevento_usgs=[]
    #time.sleep(15)
    if eventos_USGS:
        for i, evento_USGS in enumerate(eventos_USGS, 1):
            # La información principal del evento está en 'properties'
            propiedades_USGS = evento_USGS['properties']
            coordenadas_USGS = evento_USGS['geometry']
            
            # Formatea la hora de origen (está en milisegundos Unix)
            # USGS a menudo usa milisegundos, aunque el estándar FDSN es segundos.
            # se asume que el formato estándar FDSN-Event donde 'time' es un string ISO 8601.
            
            # Extracción de parámetros con valor por defecto para evitar NoneType (no lo hace en este momento para todos los parametros)
            fecha_hora = propiedades_USGS.get('time')
            tipomag = propiedades_USGS.get('magType', 'ND') # ND = No Determinado
            lugar = propiedades_USGS.get('place', 'Región Desconocida') # Usando 'place' para USGS
            agencia_fuente = propiedades_USGS.get('auth', 'NEIC')

            # Extracción y redondeo: Usar 0.0 como valor por defecto si la clave falta ejemplo lat = round(coordenadas[1], 0.0, 3)
            coordenadas = coordenadas_USGS.get('coordinates') # las coordenadas y la profundidad no estan en properties si no que en geometry
            lat = round(coordenadas[1], 3)
            lon = round(coordenadas[0], 3)
            profundidad = round(coordenadas[2], 1)
            magnitud = round(propiedades_USGS.get('mag', 0.0), 3)
             
            # se extrae la fecha/hora
            fecha_hora = propiedades_USGS.get('time')

            # Valida el tipo de dato y maneja si es nulo o numérico
            if fecha_hora is None:
                # Si es None, saltamos el evento
                continue

            # Si es un número (tiempo UNIX, generalmente milisegundos), lo convertimos a datetime
            # y luego a string ISO 8601 antes de limpiarlo.
            if isinstance(fecha_hora, (int, float)):
                # se asume que es tiempo Unix en milisegundos (común en APIs)
                # convierte milisegundos a segundos para datetime.fromtimestamp
                timestamp_segundos = fecha_hora / 1000.0 
                
                # Crear el objeto datetime
                fechahora_obj = datetime.datetime.fromtimestamp(timestamp_segundos, timezone.utc)
                
                # Formatear como string ISO 8601 para que el resto del código funcione
                # Usamos un formato estándar que incluye milisegundos y la 'Z'
                fecha_hora_str = fechahora_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                
                fecha_hora = fecha_hora_str # Sobreescribe la variable con la cadena
                
            # Si es una cadena o si ya la convertimos arriba
            if isinstance(fecha_hora, str):
                
                # elimina letra Z en el formato si la encuentra
                fecha_hora_limpia = fecha_hora.replace('Z', '')
                
                try:
                    # parsea con milisegundos (%f)
                    fechahora_obj = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        # Si falla (no hay milisegundos), intenta parsear sin milisegundos
                        fechahora_obj = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        continue # Si el formato es totalmente incorrecto, salta el evento

                # Formato de salida con UN SOLO espacio
                fechahora_str = fechahora_obj.strftime("%Y-%m-%d %H:%M:%S")

                lista = (fechahora_str, lat, lon, profundidad, magnitud, tipomag, lugar, agencia_fuente)
                listaevento_usgs.append(lista)

        # Crea y nombra el DataFrame
        df_usgs = pd.DataFrame(listaevento_usgs)
        df_usgs.columns = ['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']

        # convierte a datetime y ordena por Fecha_Hora
        df_usgs['Fecha_Hora'] = pd.to_datetime(df_usgs['Fecha_Hora'])
        df_usgs = df_usgs.sort_values(by='Fecha_Hora', ascending=True) 

        # resetea el índice del dataframe
        # 'drop=False' mantiene el índice anterior como una nueva columna (que no usaremos).
        # 'inplace=True' modifica el DataFrame directamente.
        df_usgs.reset_index(drop=True, inplace=True) 

        # crear el archivo .csv
        salida = 'consultaapi_NEIC.csv'
        df_usgs.to_csv(salida, index=True)
        
    else:
        print("No se encontraron eventos sísmicos que coincidan con los criterios de búsqueda.")

    # procesa los datos obtenidos con la consulta a la API del GFZ
    try:
        # ejecutar la solicitud con el formato text
        parametros_GFZ['format'] = 'text' # Asegura que el parámetro es 'text'
        response = requests.get(BASE_URL_GFZ, params=parametros_GFZ, timeout=30)
        response.raise_for_status() 
        
        # lee la respuesta como texto (que es un CSV delimitado por '|')
        datos_csv = response.text 
        
        # usa StringIO y pandas para leer el texto directamente como DataFrame
        from io import StringIO
        
        # df_gfz se crea directamente del texto
        # sep='|' define el delimitador (separador)
        # comment='#' ignora las líneas que comienzan con '#' (el encabezado o comentarios)
        df_gfz = pd.read_csv(StringIO(datos_csv), sep='|', comment='#')
        nombre_columnas=df_gfz.columns
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud HTTP o de conexión: {e}")
        exit()
    except Exception as e:
        print(f"❌ Error al procesar el texto CSV: {e}")
        exit()

    # estos son los datos obtenidos con la consulta a la API del GFZ
    df_gfz.columns = ['EventID', 'Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 
                    'Author', 'Catalog', 'Contributor', 'ContributorID', 
                    'Tipo Mag.', 'Mag.', 'MagAuthor', 'Referencia', 'otro']

    # elimino las columnas que no necesito y creo un nuevo dataframe para luego reordenar las columnas que se mantienen en el dataframe
    # creando un nuevo dataframe reordenado
    columnas_a_eliminar = ['EventID', 'Author', 'MagAuthor', 'Catalog', 'ContributorID', 'otro']
    df_filtrado = df_gfz.drop(columns=columnas_a_eliminar)
    df_filtrado.rename(columns={'Contributor': 'Agencia'}, inplace=True)
    columnas_actuales=df_filtrado.columns.tolist()
    nuevo_orden=['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']
    df_reordenado = df_filtrado[nuevo_orden]

    # se ordenan por Fecha_Hora
    df_reordenado['Fecha_Hora'] = pd.to_datetime(df_reordenado['Fecha_Hora'])
    df_reordenado = df_reordenado.sort_values(by='Fecha_Hora', ascending=True)

    # resetea el índice ecesario para la numeración en el dataframe
    df_reordenado.reset_index(drop=True, inplace=True) 

    # crea la columna 'Numero_Fila'
    #df_reordenado['Numero_Fila'] = df_reordenado.index + 0

    # Obtener las columnas actuales y asegurar que 'Numero_Fila' sea la primera.
    #columnas_gfz = ['Numero_Fila'] + [col for col in df_reordenado.columns if col != 'Numero_Fila']

    # aplica el nuevo orden al DataFrame
    df_final = df_reordenado # El DataFrame final y limpio se llama df_final

    # se reordena por Fecha_Hora
    df_final['Fecha_Hora'] = pd.to_datetime(df_final['Fecha_Hora'])

    # Aplica formato deseado para fecha y numero de decimales en la magnitud
    df_final['Fecha_Hora'] = df_final['Fecha_Hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_final['Mag.'] = df_final['Mag.'].round(1)

    conteo_filas = df_final.shape[0]
    if conteo_filas > 0:
        print(f"Solicitud exitosa, eventos encontrados en GFZ {conteo_filas}\n")
    
    # crea el archivo .csv
    salida = 'consultaapi_GFZ.csv'
    # mantiene index=False ya que nueva columna 'Numero_Fila' es la que se usara
    df_final.to_csv(salida, index=True)
        
except requests.exceptions.HTTPError as errh:
    print(f"❌ Error HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"❌ Error de Conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"❌ Tiempo de Espera Agotado: {errt}")
except requests.exceptions.RequestException as err:
    print(f"❌ Error General: {err}")
except json.JSONDecodeError:
    print("❌ Error al decodificar la respuesta JSON. El servicio puede haber devuelto un formato inesperado.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")
