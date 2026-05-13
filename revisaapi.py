import csv
import pandas as pd
import sys, os
from os import remove
import time
import shutil
import datetime
from datetime import timedelta
#from num2words import num2words
#listaoutrangofull.csv

def rellena(archivo, csvreader, listacsv, diccsv, agencia):
    print('entro')
    numsis_csv=0

    for linea in csvreader:

        print('linea origen', file=sys.stderr)
        print(linea,'\n', file=sys.stderr)

        cambios='n'
        cambioslat='n'
        cambioslon='n'

        """
        if linea[1]=='2026-02-28 20:21:50':
        #if agencia =='CSN':
            print('***************************', file=sys.stderr)
            print(linea, file=sys.stderr)
            print(linea[2], file=sys.stderr)
            print('largo:', len(linea[2]), file=sys.stderr)
            print(linea[3], file=sys.stderr)
            print('largo:', len(linea[3]), file=sys.stderr)
            sys.stderr.flush()
            time.sleep(60)
        """

        # Completa con ceros la latitud
        if len(linea[2])<=6:
            largo_lat=len(linea[2])
            if largo_lat==3:
                latitud=linea[2]+".000"
            if largo_lat==4:
                latitud=linea[2]+"000"
            if largo_lat==5:
                latitud=linea[2]+"00"
            if largo_lat==6:
                latitud=linea[2]+"0"
            cambios='s'
            cambioslat='s'
        else:
            if len(linea[2])>7:
                latitud=round(float(linea[2]),3)
                latitud=str(latitud)
                if len(latitud)<=6:
                    largo_latitud=len(latitud)
                    if largo_latitud==3:
                        latitud=latitud+".000"
                    if largo_latitud==4:
                        latitud=latitud+"000"
                    if largo_latitud==5:
                        latitud=latitud+"00"
                    if largo_latitud==6:
                        latitud=latitud+"0"
                cambios='s'
                cambioslat='s'
            else:
                cambios='n'
                cambioslat='n'

        # Completa con ceros la longitud
        if len(linea[3])<=6:
            largo_lon=len(linea[3])
            if largo_lon==3:
                longitud=linea[3]+".000"
            if largo_lon==4:
                longitud=linea[3]+"000"
            if largo_lon==5:
                longitud=linea[3]+"00"
            if largo_lon==6:
                longitud=linea[3]+"0"
            cambios='s'
            cambioslon='s'    
        else:
            if len(linea[3])>7:
                longitud=round(float(linea[3]),3)
                longitud=str(longitud)
                if len(longitud)<=6:
                    largo_longitud=len(longitud)
                    if largo_longitud==3:
                        longitud=longitud+".000"
                    if largo_longitud==4:
                        longitud=longitud+"000"
                    if largo_longitud==5:
                        longitud=longitud+"00"
                    if largo_longitud==6:
                        longitud=longitud+"0"
                cambios='s'
                cambioslon='s'
            else:
                if cambios!='s':
                    cambios='n'
                cambioslon='n'
        
        prof=round(float(linea[4]),1)
        prof=str(prof)

        if cambios == 's':
            if cambioslat=='s' and cambioslon=='s':
                if agencia!='listaoutrangofull':
                    diccsv={
                        "fecha_hora":linea[1],
                        "lat":latitud,
                        "lon":longitud,
                        "prof":prof,
                        "mag":linea[5],
                        "tipo_mag":linea[6],
                        "ref":linea[7],
                        "agencia":linea[8],
                    }
                else:
                    diccsv={
                        "fecha_hora":linea[1],
                        "lat":latitud,
                        "lon":longitud,
                        "prof":prof,
                        "mag":linea[5],
                        "tipo_mag":linea[6],
                        "ref":linea[7],
                        "agencia":linea[8],
                        "consulta":linea[9],
                        "asociado":linea[10],
                        "fuerarangos":'',
                        #"fuerarangos":linea[11],
                    }
            else:
                if cambioslat=='s':
                    if agencia!='listaoutrangofull':
                        diccsv={
                            "fecha_hora":linea[1],
                            "lat":latitud,
                            "lon":linea[3],
                            "prof":prof,
                            "mag":linea[5],
                            "tipo_mag":linea[6],
                            "ref":linea[7],
                            "agencia":linea[8],
                        }
                    else:
                        diccsv={
                            "fecha_hora":linea[1],
                            "lat":latitud,
                            "lon":linea[3],
                            "prof":prof,
                            "mag":linea[5],
                            "tipo_mag":linea[6],
                            "ref":linea[7],
                            "agencia":linea[8],
                            "consulta":linea[9],
                            "asociado":linea[10],
                            "fuerarangos":'',
                            #"fuerarangos":linea[11],
                        }
                else:
                    if agencia!='listaoutrangofull':
                        diccsv={
                            "fecha_hora":linea[1],
                            "lat":linea[2],
                            "lon":longitud,
                            "prof":prof,
                            "mag":linea[5],
                            "tipo_mag":linea[6],
                            "ref":linea[7],
                            "agencia":linea[8],
                        }
                    else:
                        diccsv={
                            "fecha_hora":linea[1],
                            "lat":linea[2],
                            "lon":longitud,
                            "prof":prof,
                            "mag":linea[5],
                            "tipo_mag":linea[6],
                            "ref":linea[7],
                            "agencia":linea[8],
                            "consulta":linea[9],
                            "asociado":linea[10],
                            "fuerarangos":'',
                            #"fuerarangos":linea[11],
                        }
        else:
            if agencia!='listaoutrangofull':
                diccsv={
                    "fecha_hora":linea[1],
                    "lat":linea[2],
                    "lon":linea[3],
                    "prof":prof,
                    "mag":linea[5],
                    "tipo_mag":linea[6],
                    "ref":linea[7],
                    "agencia":linea[8],
                }
            else:
                diccsv={
                    "fecha_hora":linea[1],
                    "lat":linea[2],
                    "lon":linea[3],
                    "prof":prof,
                    "mag":linea[5],
                    "tipo_mag":linea[6],
                    "ref":linea[7],
                    "agencia":linea[8],
                    "consulta":linea[9],
                    "asociado":linea[10],
                    "fuerarangos":'',
                    #"fuerarangos":linea[11],
                }
        
        print('lat:',linea[2],'\n', file=sys.stderr)
        print('lon:',linea[3],'\n', file=sys.stderr)
        print(diccsv,'\n', file=sys.stderr)
        print(cambios,'/',cambioslat,'/', cambioslon,'\n', file=sys.stderr)
        listacsv.append(diccsv)
        
        sys.stderr.flush()
    
    print ('*** nueva lista ***', agencia, file=sys.stderr)
    for sismo in listacsv:
        #print (sismo, file=sys.stderr)
        numsis_csv+=1

    if agencia=='CSN':
        print('total eventos', archivo, numsis_csv, "( fuente datos consulta eventquery )", file=sys.stderr)
    else:
        print('total eventos', archivo, numsis_csv, "( fuente datos consultaapi", agencia,")", file=sys.stderr)

    #time.sleep(30)
    return(numsis_csv, listacsv, diccsv)        

def revisando(agencias, agencia, elemento, listafinal, listaoutrango):
    fila_procesada={}
    rep_datosapi_csn=0
    rep_datosapi_csn_total=0
    avance=0

    # encuentra cual es eñ nombre de la agencia que se usara como base (la con mas soluciones) y la agencia que se ira agregando al listado final 
    for clave, info in agencias.items():
        
        if info["nombre"] == elemento:
            claveagencia2 = clave

        if info["nombre"] == agencia:
            claveagenciabase = clave

    #time.sleep(20)

    # revisando datos extraidos del EMSC que seran comparados con los los eventos de las demas agencias
    avance=0
    for sismo2 in agencias[claveagenciabase]["lista"]: # agencia base (la que tiene mas soluciones en el cuadrante de la consulta)
        print(sismo2, file=sys.stderr)
        #time.sleep(10)
        rep_datosapi_csn=0
        delta_dia=0
        delta_segundos=0
        avance=avance+1
        poravance=(avance*100)/agencias[claveagenciabase]["numeventos"]
        hora_2=sismo2['fecha_hora']
        hora_2=datetime.datetime.strptime(hora_2, '%Y-%m-%d  %H:%M:%S')
        mag2=float(sismo2['mag'])
        prof2=float(sismo2['prof'])
        #porcenprof2=(50*prof2)/100
        
        for sismo1 in agencias[claveagencia2]["lista"]:
            print(sismo1, file=sys.stderr)
            #time.sleep(10)
            hora_1=sismo1['fecha_hora']
            hora_1=datetime.datetime.strptime(hora_1, '%Y-%m-%d  %H:%M:%S')
            mag1=float(sismo1['mag'])
            prof1=float(sismo1['prof'])
            #porcenprof1=(50*prof1)/100

            valordifmag=abs(mag1-mag2)
            valordifprof=abs(prof1-prof2)

            #valor2=(valordifprof*100)/prof2
            #valor1=(valordifprof*100)/prof1

            deltatiempo1=hora_2-hora_1
            deltatiempo2=hora_1-hora_2

            deltadias1=deltatiempo1.days
            deltaminutos1=deltatiempo1.min
            deltasegundos1=deltatiempo1.total_seconds()

            deltadias2=deltatiempo2.days
            deltaminutos2=deltatiempo2.min
            deltasegundos2=deltatiempo2.total_seconds()

            # Ventana de 6 segundos para filtrar posibles eventos repetidos
            if (deltadias1 == 0 or deltadias2 == 0) and ((deltasegundos1 >=0 and deltasegundos1 <=6) or (deltasegundos2 >= 0 and deltasegundos2 <= 6)):
                #time.sleep(5)
                lat2=float(sismo2['lat'])
                lat1=float(sismo1['lat'])
                lon2=float(sismo2['lon'])
                lon1=float(sismo1['lon'])
                delta_lat=round((lat2*(-1))-(lat1*(-1)),3)
                delta_lon=round((lon2*(-1))-(lon1*(-1)),3)

                if delta_lat<0:
                    delta_lat=delta_lat*(-1)
                
                if delta_lon<0:
                    delta_lon=delta_lon*(-1)
                
                # Delta 0 en dia, de 0.700 en coordenadas de latitud y longitud , 0.5 en magnitud y que la dif. entre ambas profundidades sea menos del 50 % em ambas (revisar esta ultima condicion)
                #if (deltadias1 == 0 or deltadias2 == 0) and (delta_lat >= 0 and delta_lat <= 0.700) and (delta_lon >= 0 and delta_lon <= 0.700) and valordifmag <= 0.5 and (valor1 <= 50 or valor2 <= 50):
                if (deltadias1 == 0 or deltadias2 == 0) and (delta_lat >= 0 and delta_lat <= 0.250) and (delta_lon >= 0 and delta_lon <= 0.250) and valordifmag <= 0.2:
                #if (deltasegundos1 >= 3 or deltasegundos2 >=3) and (deltadias1 == 0 or deltadias2 == 0) and (delta_lat >= 0 and delta_lat <= 0.700) and (delta_lon >= 0 and delta_lon <= 0.700) and valordifmag <= 0.5:    
                    # elemento es la sigla de la agencia que esta dentro del nombre del archivo que se esta procesando 
                    fila_procesada = {
                        #'id': int(fila[0])+1,
                        'fecha hora': sismo1['fecha_hora'],
                        'latitud': sismo1['lat'],
                        'longitud': sismo1['lon'],
                        'prof': sismo1['prof'],
                        'magnitud': sismo1['mag'],
                        'tipo': sismo1['tipo_mag'],
                        'ref': sismo1['ref'],
                        'agencia': sismo1['agencia'],
                        'consulta': elemento,
                    }
                    #sismo1['fecha_hora']=sismo1['fecha_hora'].replace(' ', '  ')
                    #archivo3.write(sismo1['fecha_hora']+' '+sismo1['lat']+' '+sismo1['lon']+' '+sismo1['prof']+' '+sismo1['mag']+' '+sismo1['tipo_mag']+' '+sismo1['ref']+' '+sismo1['agencia']+' '+fila_procesada['consulta']+"\n")

                    listafinal.append(fila_procesada)
                    #rep_datosapi_csn=rep_datosapi_csn+1
                    
                else:

                    # aunque no cumpla con las condiciones se guarda en el csv final donde se consolidan todos lo eventos de las agencias
                    fila_procesada = {
                        #'id': int(fila[0])+1,
                        'fecha hora': sismo1['fecha_hora'],
                        'latitud': sismo1['lat'],
                        'longitud': sismo1['lon'],
                        'prof': sismo1['prof'],
                        'magnitud': sismo1['mag'],
                        'tipo': sismo1['tipo_mag'],
                        'ref': sismo1['ref'],
                        'agencia': sismo1['agencia'],
                        'consulta': elemento,
                    }
                    listafinal.append(fila_procesada)
                    #rep_datosapi_csn=rep_datosapi_csn+1

                    #if not (delta_lat >= 2) or not (delta_lon >= 2):
                    ########################
                    #time.sleep(10)
                    # guarda en una variable los parametros fuera de los rango definidos
                    parametros=''
                    fuerarango=''
                    
                    if (deltasegundos1 >= 3 and deltasegundos2 <= 3):
                        parametros=parametros+'time-'
                        fuerarango='s'

                    if not (delta_lat >= 0 and delta_lat <= 0.250):
                        parametros=parametros+'lat-'
                        fuerarango='s'
                    
                    if not (delta_lon >= 0 and delta_lon <= 0.250):
                        parametros=parametros+'lon-'
                        fuerarango='s'

                    if not valordifmag <= 0.2:
                        parametros=parametros+'mag-'
                    
                    parametros=parametros[0:-1]
                    
                    """
                    if  len(parametros)!=0:
                        print('delta_lat', delta_lat, file=sys.stderr)
                        print('delta_lon', delta_lon, file=sys.stderr)
                        print('valordifmag', valordifmag, file=sys.stderr)
                        print('parametros', parametros, file=sys.stderr)
                        time.sleep(10)      
                    """

                    if fuerarango=='s':
                        # crear csv con los eventos que se diferencian en hora, coordenadas y magnitud por sobre los limites definidos (6 min - 0.700 lat y lon - 0.5 en mag)
                        fila_procesada_out = {
                            #'id': int(fila[0])+1,
                            'fecha hora': sismo1['fecha_hora'],
                            'latitud': sismo1['lat'],
                            'longitud': sismo1['lon'],
                            'prof': sismo1['prof'],
                            'magnitud': sismo1['mag'],
                            'tipo': sismo1['tipo_mag'],
                            'ref': sismo1['ref'],
                            'agencia': sismo1['agencia'],
                            'consulta': elemento,
                            'paramout': parametros # guarda la variable dentro del diccionario que se almacenara finalmente en el csv de salida
                        }
                        print('delta_lat', delta_lat, file=sys.stderr)
                        print('delta_lon', delta_lon, file=sys.stderr)
                        print('valordifmag', valordifmag, file=sys.stderr)
                        print('parametros', parametros, file=sys.stderr)
                        time.sleep(10)
                        listaoutrango.append(fila_procesada_out)

        rep_datosapi_csn=0
    
    return listafinal, listaoutrango

# crea nuevo csv desde eventquery con nueva estructura similar a las otras consultas a las apis
#csv_file_csn = open(sys.argv[1])
csv_file_csn = open(sys.argv[1])
csvreader_csn = csv.reader(csv_file_csn)
next(csvreader_csn,None)
listacsn=[]

for lineacsn in csvreader_csn:
    fecha_hora=lineacsn[1].replace('  ', ' ')
    mag=round(float(lineacsn[5]),1)
    fila_procesada_csn= {
        #'id': int(fila[0])+1,
        'fecha hora': fecha_hora,
        'latitud': lineacsn[2],
        'longitud': lineacsn[3],
        'prof': lineacsn[4],
        'magnitud': mag,
        'tipo': lineacsn[6],
        'ref': lineacsn[7],
        'agencia': 'CSN',
    }
    listacsn.append(fila_procesada_csn)

# crear dataframe con listafinal
df_csn = pd.DataFrame(listacsn)
nombres_columnas = [
    'Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 
    'Tipo Mag.', 'Referencia', 'Agencia' # Orden final de los elementos en la lista
]
df_csn.columns = nombres_columnas
# asegura el tipo de dato (si es necesario)
df_csn['Fecha_Hora'] = pd.to_datetime(df_csn['Fecha_Hora'])

# ordena de forma ascendente (el evento más antiguo primero)
df_final_csn = df_csn.sort_values(by='Fecha_Hora', ascending=True)
df_final_csn.reset_index(drop=True, inplace=True) # reseteo el indice luego de ordenar el dataframe por Fecha_Hora

salida='consultaapi_CSN.csv'
df_final_csn.to_csv(salida, index=True)

fecha_inicio = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
path_ejecucion=os.getcwd()
listado = os.listdir(path_ejecucion)
nombres_filtrados = [
        nombre 
        for nombre in listado 
        if nombre.lower().startswith('consultaapi_') and nombre.lower().endswith('.csv')
    ]
# Estos SIEMPRE los verás en la terminal, no importa si guardas el resultado en un CSV
print(f"Archivos encontrados: {len(nombres_filtrados)}", file=sys.stderr)
print(f"Contenido: {nombres_filtrados}", file=sys.stderr)

# Forzamos que se envíen de inmediato
sys.stderr.flush()

try:
    csv_file_1 = open(nombres_filtrados[0])
    csv_file_2 = open(nombres_filtrados[1])
    csv_file_3 = open(nombres_filtrados[2])
    csv_file_4 = open(nombres_filtrados[3])
except IndexError:
    print("ERROR: No se encontraron los 4 archivos necesarios para continuar.", file=sys.stderr)
    sys.exit(1)

csvreader_1 = csv.reader(csv_file_1)
csvreader_2 = csv.reader(csv_file_2)
csvreader_3 = csv.reader(csv_file_3)
csvreader_4 = csv.reader(csv_file_4)

# saltar el encabezado
next(csvreader_1,None)
next(csvreader_2,None)
next(csvreader_3,None)
next(csvreader_4,None)

# Declara diccionario
diccsv_1={}
diccsv_2={}
diccsv_3={}
diccsv_4={}

# Declara listas
listacsv_1=[]
listacsv_2=[]
listacsv_3=[]
listacsv_4=[]

numsis_csv_1=0
numsis_csv_2=0
numsis_csv_3=0
numsis_csv_4=0

"""
# llama a funcion que completa con ceros en latitud y longitud
print('nombresfiltrados')
print(nombres_filtrados)
print('paso')
numsis_csv_1, listacsv_1, diccsv_1 = rellena(nombres_filtrados[0], csvreader_1, listacsv_1, diccsv_1, nombres_filtrados[0][12:nombres_filtrados[0].find('.')])
print(nombres_filtrados[0])
print(listacsv_1)
numsis_csv_2, listacsv_2, diccsv_2 = rellena(nombres_filtrados[1], csvreader_2, listacsv_2, diccsv_2, nombres_filtrados[1][12:nombres_filtrados[1].find('.')])
print(nombres_filtrados[1])
print(listacsv_2)
numsis_csv_3, listacsv_3, diccsv_3 = rellena(nombres_filtrados[2], csvreader_3, listacsv_3, diccsv_3, nombres_filtrados[2][12:nombres_filtrados[2].find('.')])
print(nombres_filtrados[2])
print(listacsv_3)
numsis_csv_4, listacsv_4, diccsv_4 = rellena(nombres_filtrados[3], csvreader_4, listacsv_4, diccsv_4, nombres_filtrados[3][12:nombres_filtrados[3].find('.')])
print(nombres_filtrados[3])
print(listacsv_4)
"""

# Asegurarnos de que los archivos estén al inicio antes de leerlos
csv_file_1.seek(0)
csv_file_2.seek(0)
csv_file_3.seek(0)
csv_file_4.seek(0)

# Re-generar los lectores para asegurar que están frescos
csvreader_1 = csv.reader(csv_file_1)
csvreader_2 = csv.reader(csv_file_2)
csvreader_3 = csv.reader(csv_file_3)
csvreader_4 = csv.reader(csv_file_4)

# Saltar encabezados nuevamente
next(csvreader_1, None)
next(csvreader_2, None)
next(csvreader_3, None)
next(csvreader_4, None)

numsis_csv_1, listacsv_1, diccsv_1 = rellena(nombres_filtrados[0], csvreader_1, listacsv_1, diccsv_1, nombres_filtrados[0][12:nombres_filtrados[0].find('.')])
print(f"Archivo: {nombres_filtrados[0]} | Eventos: {numsis_csv_1}", file=sys.stderr)
print(nombres_filtrados[0][12:nombres_filtrados[0].find('.')], file=sys.stderr)
#for evento in listacsv_1:
#    print(evento, file=sys.stderr)
#time.sleep(30)
# Borra archivo csv y crea uno nuevo con las columnas lon, lat y prof con decimales definidos anteriormente
if os.path.exists(nombres_filtrados[0]):
    os.remove(nombres_filtrados[0])
    #print(f"Archivo {nombres_filtrados[0]} borrado.", file=sys.stderr)
else:
    print(f"El archivo {nombres_filtrados[0]} no existe.", file=sys.stderr)

# Convierte la lista de diccionarios a un DataFrame
df_temp_1 = pd.DataFrame(listacsv_1)

# Guarda como CSV
# index=False evita que se agregue una columna extra con los números de fila
nombre_salida = nombres_filtrados[0]
df_temp_1.to_csv(nombre_salida, index=False, encoding='utf-8')
#print(f"Archivo guardado exitosamente: {nombre_salida}", file=sys.stderr)

numsis_csv_2, listacsv_2, diccsv_2 = rellena(nombres_filtrados[1], csvreader_2, listacsv_2, diccsv_2, nombres_filtrados[1][12:nombres_filtrados[1].find('.')])
print(f"Archivo: {nombres_filtrados[1]} | Eventos: {numsis_csv_2}", file=sys.stderr)
print(nombres_filtrados[0][12:nombres_filtrados[0].find('.')], file=sys.stderr)
#for evento in listacsv_2:
#    print(evento, file=sys.stderr)
#time.sleep(30)
# Borra archivo csv y crea uno nuevo con las columnas lon, lat y prof con decimales definidos anteriormente
if os.path.exists(nombres_filtrados[1]):
    os.remove(nombres_filtrados[1])
    #print(f"Archivo {nombres_filtrados[0]} borrado.", file=sys.stderr)
else:
    print(f"El archivo {nombres_filtrados[1]} no existe.", file=sys.stderr)

# Convierte la lista de diccionarios a un DataFrame
df_temp_2 = pd.DataFrame(listacsv_2)

# Guarda como CSV
# index=False evita que se agregue una columna extra con los números de fila
nombre_salida = nombres_filtrados[1]
df_temp_2.to_csv(nombre_salida, index=False, encoding='utf-8')
#print(f"Archivo guardado exitosamente: {nombre_salida}", file=sys.stderr)

numsis_csv_3, listacsv_3, diccsv_3 = rellena(nombres_filtrados[2], csvreader_3, listacsv_3, diccsv_3, nombres_filtrados[2][12:nombres_filtrados[2].find('.')])
print(f"Archivo: {nombres_filtrados[2]} | Eventos: {numsis_csv_3}", file=sys.stderr)
print(nombres_filtrados[0][12:nombres_filtrados[0].find('.')], file=sys.stderr)
#for evento in listacsv_3:
#    print(evento, file=sys.stderr)
#time.sleep(30)
# Borra archivo csv y crea uno nuevo con las columnas lon, lat y prof con decimales definidos anteriormente
if os.path.exists(nombres_filtrados[2]):
    os.remove(nombres_filtrados[2])
    #print(f"Archivo {nombres_filtrados[0]} borrado.", file=sys.stderr)
else:
    print(f"El archivo {nombres_filtrados[2]} no existe.", file=sys.stderr)

# Convierte la lista de diccionarios a un DataFrame
df_temp_3 = pd.DataFrame(listacsv_3)

# Guarda como CSV
# index=False evita que se agregue una columna extra con los números de fila
nombre_salida = nombres_filtrados[2]
df_temp_3.to_csv(nombre_salida, index=False, encoding='utf-8')
#print(f"Archivo guardado exitosamente: {nombre_salida}", file=sys.stderr)

numsis_csv_4, listacsv_4, diccsv_4 = rellena(nombres_filtrados[3], csvreader_4, listacsv_4, diccsv_4, nombres_filtrados[3][12:nombres_filtrados[3].find('.')])
print(f"Archivo: {nombres_filtrados[3]} | Eventos: {numsis_csv_4}", file=sys.stderr)
print(nombres_filtrados[0][12:nombres_filtrados[0].find('.')], file=sys.stderr)
#for evento in listacsv_4:
#    print(evento, file=sys.stderr)
#time.sleep(30)
# Borra archivo csv y crea uno nuevo con las columnas lon, lat y prof con decimales definidos anteriormente
if os.path.exists(nombres_filtrados[3]):
    os.remove(nombres_filtrados[3])
    #print(f"Archivo {nombres_filtrados[0]} borrado.", file=sys.stderr)
else:
    print(f"El archivo {nombres_filtrados[3]} no existe.", file=sys.stderr)

# Convierte la lista de diccionarios a un DataFrame
df_temp_3 = pd.DataFrame(listacsv_4)

# Guarda como CSV
# index=False evita que se agregue una columna extra con los números de fila
nombre_salida = nombres_filtrados[3]
df_temp_3.to_csv(nombre_salida, index=False, encoding='utf-8')
#print(f"Archivo guardado exitosamente: {nombre_salida}", file=sys.stderr)

# Forzamos que se envíen de inmediato
#sys.stderr.flush()
#time.sleep(30)

agencias = {
    "uno" : {
        "nombre" : nombres_filtrados[0][12:nombres_filtrados[0].find('.')],
        "numeventos" : numsis_csv_1,
        "lista": listacsv_1,
    },
    "dos" : {
        "nombre" : nombres_filtrados[1][12:nombres_filtrados[1].find('.')],
        "numeventos" : numsis_csv_2,
        "lista": listacsv_2,
    },
    "tres" : {
        "nombre" : nombres_filtrados[2][12:nombres_filtrados[2].find('.')],
        "numeventos" : numsis_csv_3,
        "lista": listacsv_3,
    },
    "cuatro" : {
        "nombre" : nombres_filtrados[3][12:nombres_filtrados[3].find('.')],
        "numeventos" : numsis_csv_4,
        "lista": listacsv_4,
    },
}    

# determina la agencia que tiene mas eventos en su consulta incluido los datos del eventquery
maximo=0
for clave, valor in agencias.items():
    nombre_agencia = valor["nombre"]
    conteo_eventos = valor["numeventos"]
    if conteo_eventos>=maximo:
        maximo=conteo_eventos
        agencia=nombre_agencia

print('\n',agencia, 'sera utilizada como base en la revisión ya que tiene', maximo, 'eventos', file=sys.stderr)

nuevalista=[]
for elemento in nombres_filtrados:
    if elemento.find(agencia)==-1:
        nuevalista.append(elemento)

listaoutrango=[]
listafinal=[]
listaoutrangofull=[]

# Este bucle llama a la funcion que va comparando las soluciones de eventos y en ella se definen margenes que consideran si un evento tiene diferencias
# que se considerarian importantes de revisar
for elemento in nuevalista:
    nombre_agencia = elemento[12:elemento.find('.')]
    # Enviamos a stderr para que aparezca en pantalla inmediatamente y no ensucie la variable de Bash
    print(f"\nProcesando: {nombre_agencia} ✅", file=sys.stderr, end='')
    revisando(agencias, agencia, nombre_agencia, listafinal, listaoutrango)


# lista de eventos fuera de rango con respecto a otras agencias
outrango=0
for i in listaoutrango:
    #print(type(i))
    #print(i)
    outrango+=1
print(f'\nEventos fuera de los rangos definidos (tiempo/lat/lon/mag): {outrango}', file=sys.stderr, end='')

for clave, info in agencias.items():
    if info["nombre"] == agencia:
        claveagenciabase = clave 

for sismo1 in agencias[claveagenciabase]["lista"]:
    fila_procesada = {
        #'id': int(fila[0])+1,
        'fecha hora': sismo1['fecha_hora'],
        'latitud': sismo1['lat'],
        'longitud': sismo1['lon'],
        'prof': sismo1['prof'],
        'magnitud': sismo1['mag'],
        'tipo': sismo1['tipo_mag'],
        'ref': sismo1['ref'],
        'agencia': sismo1['agencia'],
        'consulta': agencias[claveagenciabase]['nombre']
    }
    listafinal.append(fila_procesada)
    #archivo3.write(sismo1['fecha_hora']+' '+sismo1['lat']+' '+sismo1['lon']+' '+sismo1['prof']+' '+sismo1['mag']+' '+sismo1['tipo_mag']+' '+sismo1['ref']+' '+sismo1['agencia']+' '+agencias[claveagenciabase]['nombre']+"\n")

# crear dataframe con listafinal
df = pd.DataFrame(listafinal)
nombres_columnas = [
    'Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 
    'Tipo Mag.', 'Referencia', 'Agencia', 'Consulta' # Orden final de los elementos en la lista
]
df.columns = nombres_columnas
# asegura el tipo de dato (si es necesario)
df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'])

# ordena de forma ascendente (el evento más antiguo primero)
df_final = df.sort_values(by='Fecha_Hora', ascending=True)
df_final.reset_index(drop=True, inplace=True) # resetea el indice luego de ordenar el dataframe por Fecha_Hora

salida='listaapifinal.csv'
df_final.to_csv(salida, index=True)

# crea el txt basandose en el dataframe ordenado
# salida archivo txt
salidatxt='listaapifinal.txt'
cadena_formateada = df_final.to_string(index=False)
with open(salidatxt, 'w', encoding='utf-8') as archivo:
    archivo.write(cadena_formateada)

print(listaoutrango, file=sys.stderr)
# crear dataframe con listaoutrango
df_out_rango = pd.DataFrame(listaoutrango)
nombres_columnas = [
    'Fecha_Hora', 'Latitud', 'Longitud', 'Prof.', 'Mag.', 
    'Tipo Mag.', 'Referencia', 'Agencia', 'Consulta', 'fuerarangos' # Orden final de los elementos en la lista
]
df_out_rango.columns = nombres_columnas
# asegura el tipo de dato (si es necesario)
df_out_rango['Fecha_Hora'] = pd.to_datetime(df_out_rango['Fecha_Hora'])

# ordena de forma ascendente (el evento más antiguo primero)
df_out_rango = df_out_rango.sort_values(by='Fecha_Hora', ascending=True)
df_out_rango.reset_index(drop=True, inplace=True) # resetea el indice luego de ordenar el dataframe por Fecha_Hora

salida_out_rango='listaoutrango.csv'
df_out_rango.to_csv(salida_out_rango, index=True)

##### codigo nuevo #####
#
# se debe recorrer el csv o dataframe df_out_rango para ir revisando el df_final
# y generar un  nuevo  dataframe con los eventos cercanos en una ventana de 6 segundos



# df_final y df_out_rango deben existir

VENTANA_PROXIMIDAD = timedelta(seconds=6)
UMBRAL_GRADOS = 1.0  # 1 grago, aproximadamente 111 km
registros_cercanos_lista = []

# Convertir columnas de df_final a números
df_final['Latitud'] = pd.to_numeric(df_final['Latitud'], errors='coerce')
df_final['Longitud'] = pd.to_numeric(df_final['Longitud'], errors='coerce')

# Convertir columnas de df_out_rango a números
df_out_rango['Latitud'] = pd.to_numeric(df_out_rango['Latitud'], errors='coerce')
df_out_rango['Longitud'] = pd.to_numeric(df_out_rango['Longitud'], errors='coerce')

# Opcional: Eliminar filas que no pudieron convertirse (si hubiera basura en el texto)
df_final = df_final.dropna(subset=['Latitud', 'Longitud'])
df_out_rango = df_out_rango.dropna(subset=['Latitud', 'Longitud'])

# Buscando registros en df_final cuya Fecha_Hora esté a +/- 6 segundos de df_out_rango
indice=0

# ... (mantener conversiones de Latitud/Longitud anteriores)

for _, row_out in df_out_rango.iterrows():
    tiempo_ref = row_out['Fecha_Hora']
    lat_ref = float(row_out['Latitud'])
    lon_ref = float(row_out['Longitud'])
    valor_fuerarango = row_out['fuerarangos']

    limite_inferior = tiempo_ref - VENTANA_PROXIMIDAD
    limite_superior = tiempo_ref + VENTANA_PROXIMIDAD
    
    df_cercanos = df_final[
        (df_final['Fecha_Hora'] >= limite_inferior) & 
        (df_final['Fecha_Hora'] <= limite_superior) &
        (abs(df_final['Latitud'] - lat_ref) <= UMBRAL_GRADOS) &
        (abs(df_final['Longitud'] - lon_ref) <= UMBRAL_GRADOS)
    ].copy()

    if not df_cercanos.empty:
        # Usamos un índice para agrupar visualmente los sismos que pertenecen al mismo evento de referencia
        indice += 1 
        for _, row_match in df_cercanos.iterrows():
            if row_out['Agencia'] == row_match['Agencia'] and row_out['Fecha_Hora'] == row_match['Fecha_Hora']:
                continue
                
            asociacion = {
                "id": 0, # Placeholder para que rellena() no falle si espera un índice
                "Fecha_Hora": row_out['Fecha_Hora'],
                "Latitud": row_out['Latitud'],
                "Longitud": row_out['Longitud'],
                "prof.": row_out['Prof.'],
                "Mag.": row_out['Mag.'],
                "Tipo_Mag.": row_out['Tipo Mag.'],
                "Referencia": row_out['Referencia'],
                "Agencia": row_out['Agencia'],
                "Consulta": row_out['Consulta'],
                "Asociado": indice,
                "fuerarangos": valor_fuerarango
            }
            registros_cercanos_lista.append(asociacion)

if registros_cercanos_lista:
    # 1. Crear DataFrame inicial
    df_previo = pd.DataFrame(registros_cercanos_lista)
    salida_cercanos = 'listaoutrangofull.csv'
    
    # Guardamos temporalmente para que 'rellena' pueda leerlo como CSV
    df_previo.to_csv(salida_cercanos, index=False)

    # 2. Re-procesar con la función 'rellena' para formatear decimales
    with open(salida_cercanos, 'r') as csv_file_outrange:
        csvreader_outrange = csv.reader(csv_file_outrange)
        next(csvreader_outrange, None) # Saltar cabecera
        
        lista_out_formateada = []
        dic_out = {}
        # Llamamos a rellena con el modo 'listaoutrangofull' que ya definiste en tu función
        _, lista_out_formateada, _ = rellena(salida_cercanos, csvreader_outrange, lista_out_formateada, dic_out, 'listaoutrangofull')

    # 3. Guardar el resultado final con el formato de ceros
    df_out_final = pd.DataFrame(lista_out_formateada)
    
    # Asegurar el orden de columnas para el CSV final
    columnas_finales = [
        'fecha_hora', 'lat', 'lon', 'prof', 'mag', 
        'tipo_mag', 'ref', 'agencia', 'consulta', 'asociado', 'fuerarangos'
    ]
    
    # Reordenamos solo si las columnas existen
    df_out_final = df_out_final[columnas_finales]
    df_out_final.to_csv(salida_cercanos, index=True, encoding='utf-8')
    
    print(f"\n✅ Archivo {salida_cercanos} generado con éxito.", file=sys.stderr)
else:
    print("No se encontraron asociaciones.", file=sys.stderr)

#########################

#print("\n✅Finalizado")

fecha_termino = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S')
fecha_termino = datetime.datetime.strptime(fecha_termino, '%Y-%m-%d %H:%M:%S')
tiempo_proc=fecha_termino-fecha_inicio

#print("----------------------------------- Salida -----------------------------------")
#print('tiempo proceso:', tiempo_proc) 
#print('Posibles repetidos de EMSC en CSN:',rep_datosapi_csn_total)
#print('Archivos generados...')
#print(salidatxt)
#print(salida)
#print(salida_out_rango)
#print(salida_cercanos)

print(f"\nArchivos generados: {salidatxt}, {salida}, {salida_out_rango}, {salida_cercanos}", file=sys.stderr, end='')
#print(f"Tiempo de proceso: {tiempo_proc}", file=sys.stderr)

# 2. Imprime ÚNICAMENTE el valor que quieres que Bash reciba
# En tu caso, la variable 'agencia' que determinaste como base
print(agencia)
#time.sleep(30)
#sys.exit(agencia)
