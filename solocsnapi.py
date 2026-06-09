import pandas as pd

# cargar los archivos y limpia nombres de columnas
df_full = pd.read_csv('listaoutrangofull.csv')
df_rangos = pd.read_csv('listaoutrango.csv')

# Forzamos que todas las columnas sean minúsculas para que 'fecha_hora' siempre exista
df_full.columns = df_full.columns.str.lower()
df_rangos.columns = df_rangos.columns.str.lower()

df_full.columns = df_full.columns.str.strip()
df_rangos.columns = df_rangos.columns.str.strip()

#b identifica IDs (Asociado) que tienen reportes de CSN y otras agencias
ids_con_csn = set(df_full[df_full['consulta'] == 'CSN']['asociado'])
ids_con_otras = set(df_full[df_full['consulta'] != 'CSN']['asociado'])
ids_compartidos = ids_con_csn.intersection(ids_con_otras)

# filtra df_full para quedarnos solo con los eventos compartidos
df_compartidos = df_full[df_full['asociado'].isin(ids_compartidos)].copy()

# prepar las fechas para el cruce (asegurando que coincidan los formatos)
df_compartidos['fecha_hora'] = pd.to_datetime(df_compartidos['fecha_hora'])
df_rangos['fecha_hora'] = pd.to_datetime(df_rangos['fecha_hora'])

# cruza con listaoutrango para agregar la columna 'fuerarangos'
# se usa Fecha_Hora y Consulta como llaves únicas para evitar errores
df_final = pd.merge(
    df_compartidos, 
    df_rangos[['fecha_hora', 'consulta', 'fuerarangos']], 
    on=['fecha_hora', 'consulta'], 
    how='left'
)

# ordena por Asociado para agrupar los sismos visualmente
df_final = df_final.sort_values(by=['asociado', 'fecha_hora'])

# guardar el resultado final
df_final.to_csv('eventos_compartidos_full.csv', index=False)

"""
print(f"Proceso exitoso.")
print(f"Sismos compartidos identificados: {len(ids_compartidos)}")
print(f"Archivo 'eventos_compartidos_full.csv' generado con la columna fuerarangos.")
"""
