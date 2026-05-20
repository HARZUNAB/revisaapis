import requests
import json
import pandas as pd
import datetime
import sys, os
import csv
from io import StringIO
import time
from datetime import timezone

listaevento = []
listaevento_usgs = []

# URL base del servicio para API
BASE_URL_EMSC = "http://www.seismicportal.eu/fdsnws/event/1/query?"
BASE_URL_USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
BASE_URL_GFZ = "http://geofon.gfz.de/fdsnws/event/1/query?"

# Parámetros que vienen al ejecutar el script desde Bash
starttime = sys.argv[1]
endtime = sys.argv[2]
minmag = sys.argv[3]

# Definición de los 3 cuadrantes geográficos para cubrir todo Chile
CUADRANTES_CHILE = [
    {"name": "Continental e Insular Cercano", "minlat": -56.0, "maxlat": -17.5, "minlon": -76.0, "maxlon": -66.0},
    {"name": "Chile Insular Oceánico (Rapa Nui)", "minlat": -28.0, "maxlat": -26.0, "minlon": -110.0, "maxlon": -108.0},
    {"name": "Territorio Antártico Chileno", "minlat": -90.0, "maxlat": -60.0, "minlon": -90.0, "maxlon": -53.0}
]

# =============================================================================
# 1. CONSULTA Y PROCESAMIENTO EMSC
# =============================================================================
for cuadrante in CUADRANTES_CHILE:
    parametros_EMSC = {
        'starttime': starttime,
        'endtime': endtime,
        'minmag': minmag,
        'minlatitude': cuadrante['minlat'],
        'maxlatitude': cuadrante['maxlat'],
        'minlongitude': cuadrante['minlon'],
        'maxlongitude': cuadrante['maxlon'],
        'format': 'json'
    }
    try:
        response_EMSC = requests.get(BASE_URL_EMSC, params=parametros_EMSC, timeout=30)
        
        # Si la API confirma que no hay contenido (204), pasamos silenciosamente
        if response_EMSC.status_code == 204:
            continue
            
        response_EMSC.raise_for_status()
        texto_respuesta = response_EMSC.text.strip()
        
        # Si el cuerpo de respuesta está vacío o es una página HTML de error, controlamos el flujo
        if not texto_respuesta:
            continue
        if texto_respuesta.startswith("<html") or texto_respuesta.startswith("<!DOCTYPE html"):
            print(f"❌ EMSC ({cuadrante['name']}): El servicio web devolvió un HTML de error en lugar de datos.")
            continue
            
        datos_EMSC = response_EMSC.json()
        eventos_EMSC = datos_EMSC.get('features', [])
        
        for evento in eventos_EMSC:
            propiedades = evento['properties']
            fecha_hora = propiedades.get('time')
            lat = round(propiedades.get('lat'), 3)
            lon = round(propiedades.get('lon'), 3)
            profundidad = propiedades.get('depth')
            magnitud = propiedades.get('mag')
            tipomag = propiedades.get('magtype')
            lugar = propiedades.get('flynn_region', 'Región Desconocida')
            agencia_fuente = propiedades.get('auth')

            fecha_hora_limpia = fecha_hora.replace('Z', '')
            fechahora = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S.%f")
            fechahora_str = fechahora.strftime("%Y-%m-%d %H:%M:%S")

            lista = (fechahora_str, lat, lon, profundidad, magnitud, tipomag, lugar, agencia_fuente)
            listaevento.append(lista)
    except Exception as e:
        # Solo muestra error si hay una falla real de conexión o un estatus HTTP inválido (ej: 500, 502)
        print(f"⚠️ EMSC ({cuadrante['name']}): Error crítico en la solicitud. Detalle: {e}")

if listaevento:
    df_EMSC = pd.DataFrame(listaevento)
    df_EMSC.columns = ['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']
    df_EMSC['Fecha_Hora'] = pd.to_datetime(df_EMSC['Fecha_Hora'])
    df_EMSC = df_EMSC.drop_duplicates().sort_values(by='Fecha_Hora', ascending=True).reset_index(drop=True)
    df_EMSC.to_csv('consultaapi_EMSC.csv', index=True)
    print(f"Solicitud exitosa, eventos únicos encontrados en EMSC: {len(df_EMSC)}")
else:
    print("No se encontraron eventos sísmicos en el EMSC para los cuadrantes de Chile.")


# =============================================================================
# 2. CONSULTA Y PROCESAMIENTO USGS
# =============================================================================
for cuadrante in CUADRANTES_CHILE:
    parametros_USGS = {
        'starttime': starttime[:10],
        'endtime': endtime[:10],
        'minmag': minmag,
        'minlatitude': cuadrante['minlat'],
        'maxlatitude': cuadrante['maxlat'],
        'minlongitude': cuadrante['minlon'],
        'maxlongitude': cuadrante['maxlon'],
        'format': 'geojson'
    }
    try:
        response_USGS = requests.get(BASE_URL_USGS, params=parametros_USGS, timeout=30)
        response_USGS.raise_for_status()
        datos_USGS = response_USGS.json()
        eventos_USGS = datos_USGS.get('features', [])

        for evento_USGS in eventos_USGS:
            propiedades_USGS = evento_USGS['properties']
            coordenadas_USGS = evento_USGS['geometry']
            
            fecha_hora = propiedades_USGS.get('time')
            tipomag = propiedades_USGS.get('magType', 'ND')
            lugar = propiedades_USGS.get('place', 'Región Desconocida')
            agencia_fuente = propiedades_USGS.get('auth', 'NEIC')

            coordenadas = coordenadas_USGS.get('coordinates')
            lat = round(coordenadas[1], 3)
            lon = round(coordenadas[0], 3)
            profundidad = round(coordenadas[2], 1)
            magnitud = round(propiedades_USGS.get('mag', 0.0), 3)
             
            if fecha_hora is None:
                continue

            if isinstance(fecha_hora, (int, float)):
                timestamp_segundos = fecha_hora / 1000.0 
                fechahora_obj = datetime.datetime.fromtimestamp(timestamp_segundos, timezone.utc)
                fecha_hora = fechahora_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                
            if isinstance(fecha_hora, str):
                fecha_hora_limpia = fecha_hora.replace('Z', '')
                try:
                    fechahora_obj = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        fechahora_obj = datetime.datetime.strptime(fecha_hora_limpia, "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        continue

                fechahora_str = fechahora_obj.strftime("%Y-%m-%d %H:%M:%S")
                lista = (fechahora_str, lat, lon, profundidad, magnitud, tipomag, lugar, agencia_fuente)
                listaevento_usgs.append(lista)
    except Exception as e:
        print(f"⚠️ USGS ({cuadrante['name']}): Error de conexión o servicio. Detalle: {e}")

if listaevento_usgs:
    df_usgs = pd.DataFrame(listaevento_usgs)
    df_usgs.columns = ['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']
    df_usgs['Fecha_Hora'] = pd.to_datetime(df_usgs['Fecha_Hora'])
    df_usgs = df_usgs.drop_duplicates().sort_values(by='Fecha_Hora', ascending=True).reset_index(drop=True)
    df_usgs.to_csv('consultaapi_NEIC.csv', index=True)
    print(f"Solicitud exitosa, eventos únicos encontrados en USGS: {len(df_usgs)}")
else:
    print("No se encontraron eventos sísmicos en el USGS para los cuadrantes de Chile.")


# =============================================================================
# 3. CONSULTA Y PROCESAMIENTO GFZ
# =============================================================================
dfs_gfz_list = []
for cuadrante in CUADRANTES_CHILE:
    parametros_GFZ = {
        'starttime': starttime[:10],
        'endtime': endtime[:10],
        'minmag': minmag,
        'minlatitude': cuadrante['minlat'],
        'maxlatitude': cuadrante['maxlat'],
        'minlongitude': cuadrante['minlon'],
        'maxlongitude': cuadrante['maxlon'],
        'format': 'text'
    }
    try:
        response = requests.get(BASE_URL_GFZ, params=parametros_GFZ, timeout=30)
        response.raise_for_status() 
        datos_csv = response.text 
        
        # Si la respuesta solo contiene comentarios o está vacía, saltar
        if not datos_csv.strip() or all(line.startswith('#') for line in datos_csv.strip().split('\n')):
            continue
            
        df_temp = pd.read_csv(StringIO(datos_csv), sep='|', comment='#')
        if not df_temp.empty:
            dfs_gfz_list.append(df_temp)
    except Exception as e:
        print(f"⚠️ GFZ ({cuadrante['name']}): Error de conexión o servicio. Detalle: {e}")

if dfs_gfz_list:
    df_gfz = pd.concat(dfs_gfz_list, ignore_index=True)
    df_gfz.columns = ['EventID', 'Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 
                    'Author', 'Catalog', 'Contributor', 'ContributorID', 
                    'Tipo Mag.', 'Mag.', 'MagAuthor', 'Referencia', 'otro']

    columnas_a_eliminar = ['EventID', 'Author', 'MagAuthor', 'Catalog', 'ContributorID', 'otro']
    df_filtrado = df_gfz.drop(columns=columnas_a_eliminar)
    df_filtrado.rename(columns={'Contributor': 'Agencia'}, inplace=True)
    
    nuevo_orden = ['Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 'Tipo Mag.', 'Referencia', 'Agencia']
    df_reordenado = df_filtrado[nuevo_orden].copy()

    df_reordenado['Fecha_Hora'] = pd.to_datetime(df_reordenado['Fecha_Hora'])
    df_reordenado = df_reordenado.drop_duplicates().sort_values(by='Fecha_Hora', ascending=True).reset_index(drop=True)

    df_final = df_reordenado
    df_final['Fecha_Hora'] = df_final['Fecha_Hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_final['Mag.'] = df_final['Mag.'].round(1)

    print(f"Solicitud exitosa, eventos únicos encontrados en GFZ: {len(df_final)}\n")
    df_final.to_csv('consultaapi_GFZ.csv', index=True)
else:
    print("No se encontraron eventos sísmicos en el GFZ para los cuadrantes de Chile.\n")