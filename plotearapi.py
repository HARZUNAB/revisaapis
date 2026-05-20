from PIL import Image, ImageTk, ImageDraw, ImageGrab
import tkinter as tk
import json
import time
import sys, os
#from tkinter import messagebox
from tkinter import scrolledtext
import pandas as pd
import csv

# define ruta de mapas utilizados y directorio donde se encuenta el usuario al ejecutar el script plotear
# en este directorio deben estar los archivos .json que se generaron con anterioridad 
path_perfil="/home/hriquelmez/Desarrollo/harzmapas/perfiles_seisan"
# path mapas planta harz
path_planta="/home/hriquelmez/Desarrollo/harzmapas/planta_2"
path_ejecucion=os.getcwd()

def crear_canvas(nuevo_ancho, nuevo_alto):
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Perfil / Planta")

    # Crear el canvas perfil
    canvas = tk.Canvas(ventana, width=nuevo_ancho, height=nuevo_alto)
    canvas.pack(side=tk.LEFT)

    # Crear el canvas para planta
    canvas_planta = tk.Canvas(ventana, width=nuevo_ancho, height=nuevo_alto)
    canvas_planta.pack(side=tk.RIGHT)
    return ventana, canvas, canvas_planta

def redimensionar_imagen(imagen_path, nuevo_ancho, nuevo_alto):
    imagen = Image.open(imagen_path)
    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    return ImageTk.PhotoImage(imagen_redimensionada)

def mostrar_imagen_en_canvas(canvas, imagen_tk):
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
    canvas.image = imagen_tk  # Mantener una referencia a la imagen

def geographic_to_canvas_planta(lat, lon, min_lat, max_lat, min_lon, max_lon, canvas_width, canvas_height):
    # Convierte coordenadas geográficas (latitud, longitud) a coordenadas de píxeles en un canvas.
    # Calcula la escala para latitud y longitud
    lat_scale = (canvas_height) / (max_lat - min_lat)
    lon_scale = (canvas_width) / (max_lon - min_lon)

    # Calcula las coordenadas x e y en el canvas
    x = (lon - min_lon) * lon_scale
    y = canvas_height - ((lat - min_lat) * lat_scale)  # Invertir y para la coordenada del canvas
    return x, y

def geographic_to_canvas_perfil(x, y, minY, maxY, minX, maxX, canvas_width, canvas_height):
    # Convierte coordenadas geográficas (latitud, profundidad) a coordenadas de píxeles en un canvas.
    # Calcula la escala para longitud y profundidad
    canvasX = ((x - minX) / (maxX - minX)) * canvas_width
    canvasY = canvas_height - ((y - minY) / (maxY - minY)) * canvas_height
    return canvasX, canvasY

def ploteando(archivo_plot, perfil_plot, planta_plot, fuente, percibidos, agenciabase):

    if (fuente == "eventquery"):
        if not os.path.exists("percibidos.txt"):
            archivo_perc = open("percibidos.txt", "w")
            archivo_perc.write("id fecha hora latitud longitud prof mag tipomag percibido\n")
            archivo_perc.close()
    
    # Asigna valores para parametros del cuadrante base para canvas de perfil
    minY = perfiles_seisan[perfil_plot]["minY"]
    maxY = perfiles_seisan[perfil_plot]["maxY"]
    minX = perfiles_seisan[perfil_plot]["minX"]
    maxX = perfiles_seisan[perfil_plot]["maxX"]

    # Asigna valores para parametros del cuadrante base para canvas de planta
    min_lat = plantas[planta_plot]["minY"]
    max_lat = plantas[planta_plot]["maxY"]
    min_lon = plantas[planta_plot]["minX"]
    max_lon = plantas[planta_plot]["maxX"]

    nombre_del_archivo = path_ejecucion + "/" + archivo_plot

    total_eventos = 0
    evento_percibido = []

    with open(nombre_del_archivo) as contenido:
        eventos = json.load(contenido)
        
        # =========================================================================
        # PASO 1: MAPEADO DE COORDENADAS CSN POR EVENTO ASOCIADO
        # =========================================================================
        diccionario_csn = {}
        for ev in eventos:
            if ev.get('consulta') == 'CSN':
                id_sismo = ev.get('asociado') or ev.get('id')
                lat_val = ev.get('latitud') or ev.get('lat')
                lon_val = ev.get('longitud') or ev.get('lon')
                
                if id_sismo and lat_val and lon_val:
                    diccionario_csn[id_sismo] = {
                        'lat': float(lat_val),
                        'lon': float(lon_val)
                    }

        # =========================================================================
        # PASO 2: CONVERSIÓN A DATAFRAME Y AGRUPACIÓN POR SISMO REAL
        # Esto aísla los eventos para que no se mezclen coordenadas de sismos distintos
        # =========================================================================
        df_eventos = pd.DataFrame(eventos)
        
        if not df_eventos.empty:
            # Si no existe la columna 'asociado', respaldamos con el id
            if 'asociado' not in df_eventos.columns:
                df_eventos['asociado'] = df_eventos['id']

            # Agrupamos por el identificador del sismo
            grupos_sismos = df_eventos.groupby('asociado')

            for id_sismo, grupo in grupos_sismos:
                # 🔹 AQUÍ OCURRE LA MAGIA: Inicializamos los sets LIMPIOS para CADA SISMO
                coordenadas_perfil_usadas = set()
                coordenadas_planta_usadas = set()

                for _, evento in grupo.iterrows():
                    # Definir colores base al plotear
                    color1 = "yellow"
                    color2 = "red"
                    color3 = "blue"
                    color4 = "green"
                    color = color1
                    
                    id = evento.get('id')
                    fecha_hora = evento.get('fecha hora') or evento.get('fecha_hora')
                    lat_punto = float(evento.get('latitud') or evento.get('lat'))
                    lon_punto = float(evento.get('longitud') or evento.get('lon'))
                    prof_punto = float(evento.get('prof')) * -1
                    
                    # ---------------------------------------------------------------------
                    # SECCIÓN PERFIL
                    # ---------------------------------------------------------------------
                    x, y = geographic_to_canvas_perfil(lon_punto, prof_punto, minY, maxY, minX, maxX, nuevo_ancho, nuevo_alto)
                    
                    if perfil_plot[:10] != "sin_perfil":
                        if fuente == "eventquery" and evento.get('percibido') == "S":
                            color = color2
                        if (fuente == "todas" or fuente == "outrangos" or fuente == "outrangosfull" or fuente == "outrangosCSN") and evento.get('consulta') == "CSN":
                            color = color3
                        if (fuente == "todas" or fuente == "outrangos" or fuente == "outrangosfull" or fuente == "outrangosCSN") and evento.get('consulta') == agenciabase:
                            color = color4

                        # Detección de coincidencia local (Solo afecta a soluciones de ESTE sismo)
                        coord_actual = (round(x, 1), round(y, 1))
                        if coord_actual in coordenadas_perfil_usadas:
                            canvas.create_oval(x-8, y-8, x+8, y+8, outline="magenta", width=2)
                        else:
                            coordenadas_perfil_usadas.add(coord_actual)

                        canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="black")
                        canvas.create_text(x, y - 10, text=id, fill="black")
                        color = color1
                    
                    total_eventos = total_eventos + 1
                    
                    # Lógica de guardado de percibidos
                    if fuente == "eventquery" and evento.get('percibido') == "S":
                        color = color2
                        percibidos = percibidos + 1
                        
                        evento_procesado = {
                            'id': id, 'fecha hora': fecha_hora, 'latitud': lat_punto,
                            'longitud': lon_punto, 'prof': prof_punto,
                            'magnitud': evento.get('magnitud'), 'tipo': evento.get('tipo'),
                            'percibido': evento.get('percibido'),
                        }
                        evento_percibido.append(evento_procesado)

                        with open("percibidos.txt", "a") as archivo_perc:
                            linea_a_escribir = f"{evento_procesado['id']} {evento_procesado['fecha hora']} {evento_procesado['latitud']} {evento_procesado['longitud']} {evento_procesado['prof']} {evento_procesado['magnitud']} {evento_procesado['tipo']} {evento_procesado['percibido']}\n"
                            archivo_perc.write(linea_a_escribir)

                        color = color1

                    # ---------------------------------------------------------------------
                    # SECCIÓN PLANTA
                    # ---------------------------------------------------------------------
                    if lat_punto >= min_lat and lat_punto <= max_lat and lon_punto >= min_lon and lon_punto <= max_lon:
                        
                        x_plan, y_plan = geographic_to_canvas_planta(lat_punto, lon_punto, min_lat, max_lat, min_lon, max_lon, nuevo_ancho, nuevo_alto)
                        
                        if fuente == "eventquery" and evento.get('percibido') == "S":
                            color = color2
                        if (fuente == "todas" or fuente == "outrangos" or fuente == "outrangosfull" or fuente == "outrangosCSN") and evento.get('consulta') == "CSN":
                            color = color3
                        if (fuente == "todas" or fuente == "outrangos" or fuente == "outrangosfull" or fuente == "outrangosCSN") and evento.get('consulta') == agenciabase:
                            color = color4

                        # Dibujar la línea entre la agencia internacional y su CSN correspondiente
                        id_actual = evento.get('asociado') or evento.get('id')
                        if evento.get('consulta') != 'CSN' and id_actual in diccionario_csn:
                            lat_csn_propia = diccionario_csn[id_actual]['lat']
                            lon_csn_propia = diccionario_csn[id_actual]['lon']
                            if lat_csn_propia >= min_lat and lat_csn_propia <= max_lat and lon_csn_propia >= min_lon and lon_csn_propia <= max_lon:
                                x_csn, y_csn = geographic_to_canvas_planta(lat_csn_propia, lon_csn_propia, min_lat, max_lat, min_lon, max_lon, nuevo_ancho, nuevo_alto)
                                canvas_planta.create_line(x_plan, y_plan, x_csn, y_csn, fill="gray", dash=(4, 4))

                        # Detección de coincidencia local en Planta (Se limpia con cada sismo)
                        coord_planta_actual = (round(x_plan, 1), round(y_plan, 1))
                        if coord_planta_actual in coordenadas_planta_usadas:
                            canvas_planta.create_oval(x_plan-8, y_plan-8, x_plan+8, y_plan+8, outline="magenta", width=2)
                        else:
                            coordenadas_planta_usadas.add(coord_planta_actual)

                        # Cambiar la figura si el error es de Magnitud
                        razon_error = str(evento.get('fuerarangos'))
                        if "magnitud" in razon_error and evento.get('consulta') != 'CSN':
                            canvas_planta.create_rectangle(x_plan-5, y_plan-5, x_plan+5, y_plan+5, fill=color, outline="black")
                        else:
                            canvas_planta.create_oval(x_plan-5, y_plan-5, x_plan+5, y_plan+5, fill=color, outline="black")
             
                        texto_mapa = str(id)
                        if evento.get('fuerarangos') and pd.notna(evento.get('fuerarangos')):
                            texto_mapa = str(id) + " (" + str(evento.get('fuerarangos')) + ")"
                            
                        canvas_planta.create_text(x_plan, y_plan - 12, text=texto_mapa, fill="black")

                    color = color1

    # =========================================================================
    # LEYENDAS EXPLICATIVAS (Esquinas Inferiores de Canvas)
    # =========================================================================
    fuente_texto = ("Arial", 9, "bold")
    fuente_titulo = ("Arial", 10, "bold")

    # ---------------------------------------------------------------------
    # LEYENDA DEL CANVAS DE PERFIL (Esquina Inferior Izquierda: x=10, y=nuevo_alto-130)
    # ---------------------------------------------------------------------
    if perfil_plot[:10] != "sin_perfil":
        # Cuadro contenedor de fondo para legibilidad
        canvas.create_rectangle(10, nuevo_alto - 130, 260, nuevo_alto - 10, fill="#F0F0F0", outline="black", width=1)
        canvas.create_text(20, nuevo_alto - 115, text="LEYENDA DE SOLUCIONES", anchor=tk.W, font=fuente_titulo, fill="black")
        
        # Muestras de colores (Círculos)
        # CSN (Azul)
        canvas.create_oval(20 - 4, (nuevo_alto - 95) - 4, 20 + 4, (nuevo_alto - 95) + 4, fill="blue", outline="black")
        canvas.create_text(35, nuevo_alto - 95, text="Solución local (CSN)", anchor=tk.W, font=fuente_texto, fill="black")
        
        # Agencia Base / Internacional (Verde / Amarillo)
        canvas.create_oval(20 - 4, (nuevo_alto - 75) - 4, 20 + 4, (nuevo_alto - 75) + 4, fill="green", outline="black")
        canvas.create_text(35, nuevo_alto - 75, text=f"Solución Base ({agenciabase})", anchor=tk.W, font=fuente_texto, fill="black")
        
        # Percibidos (Rojo)
        canvas.create_oval(20 - 4, (nuevo_alto - 55) - 4, 20 + 4, (nuevo_alto - 55) + 4, fill="red", outline="black")
        canvas.create_text(35, nuevo_alto - 55, text="Evento Percibido (S)", anchor=tk.W, font=fuente_texto, fill="black")

        # Aro Magenta de Superposición
        canvas.create_oval(20 - 6, (nuevo_alto - 30) - 6, 20 + 6, (nuevo_alto - 30) + 6, outline="magenta", width=2)
        canvas.create_oval(20 - 3, (nuevo_alto - 30) - 3, 20 + 3, (nuevo_alto - 30) + 3, fill="yellow", outline="black")
        canvas.create_text(35, nuevo_alto - 30, text="Soluciones Superpuestas", anchor=tk.W, font=fuente_texto, fill="magenta")

    # =========================================================================
    # LEYENDAS EXPLICATIVAS UNIFICADAS Y SIMÉTRICAS
    # =========================================================================
    fuente_texto = ("Arial", 9, "bold")
    fuente_titulo = ("Arial", 10, "bold")

    # Dimensiones y coordenadas base para homogeneizar las cajas
    ancho_caja = 250
    alto_caja = 130

    # =========================================================================
    # LEYENDAS EXPLICATIVAS UNIFICADAS Y SIMÉTRICAS (Coordenadas Relativas)
    # =========================================================================
    fuente_texto = ("Arial", 9, "bold")
    fuente_titulo = ("Arial", 10, "bold")

    # Dimensiones fijas de las cajas de leyenda
    ancho_caja = 250
    alto_caja = 130

    # Margen interno para el espaciado vertical de los elementos
    espacio_items = 20

    # ---------------------------------------------------------------------
    # LEYENDA: CANVAS DE PERFIL (Esquina Inferior Izquierda)
    # ---------------------------------------------------------------------
    if perfil_plot[:10] != "sin_perfil":
        x_perfil_origen = 10
        y_perfil_origen = nuevo_alto - (alto_caja + 10)
        
        # Contenedor base
        canvas.create_rectangle(x_perfil_origen, y_perfil_origen, x_perfil_origen + ancho_caja, nuevo_alto - 10, fill="#F0F0F0", outline="black", width=1)
        canvas.create_text(x_perfil_origen + 10, y_perfil_origen + 15, text="LEYENDA DE SOLUCIONES", anchor=tk.W, font=fuente_titulo, fill="black")
        
        # Símbolo 1: CSN (Azul)
        y_item = y_perfil_origen + 40
        canvas.create_oval(x_perfil_origen + 15 - 4, y_item - 4, x_perfil_origen + 15 + 4, y_item + 4, fill="blue", outline="black")
        canvas.create_text(x_perfil_origen + 30, y_item, text="Solución CSN", anchor=tk.W, font=fuente_texto, fill="black")
        
        # Símbolo 2: Agencia Base (Verde)
        y_item += espacio_items
        canvas.create_oval(x_perfil_origen + 15 - 4, y_item - 4, x_perfil_origen + 15 + 4, y_item + 4, fill="green", outline="black")
        canvas.create_text(x_perfil_origen + 30, y_item, text=f"Agencia Base ({agenciabase})", anchor=tk.W, font=fuente_texto, fill="black")
        
        # Símbolo 3: Evento Percibido (Rojo)
        y_item += espacio_items
        canvas.create_oval(x_perfil_origen + 15 - 4, y_item - 4, x_perfil_origen + 15 + 4, y_item + 4, fill="red", outline="black")
        canvas.create_text(x_perfil_origen + 30, y_item, text="Evento Percibido", anchor=tk.W, font=fuente_texto, fill="black")

        # Símbolo 4: Soluciones Superpuestas (Aro Magenta + Centro Agencia)
        y_item += espacio_items
        canvas.create_oval(x_perfil_origen + 15 - 7, y_item - 7, x_perfil_origen + 15 + 7, y_item + 7, outline="magenta", width=2)
        canvas.create_oval(x_perfil_origen + 15 - 4, y_item - 4, x_perfil_origen + 15 + 4, y_item + 4, fill="green", outline="black")
        canvas.create_text(x_perfil_origen + 30, y_item, text="Soluciones Superpuestas", anchor=tk.W, font=fuente_texto, fill="magenta")

    # ---------------------------------------------------------------------
    # LEYENDA: CANVAS DE PLANTA (Esquina Inferior Derecha)
    # ---------------------------------------------------------------------
    x_planta_origen = nuevo_ancho - (ancho_caja + 10)
    y_planta_origen = nuevo_alto - (alto_caja + 10)
    
    # Contenedor base idéntico
    canvas_planta.create_rectangle(x_planta_origen, y_planta_origen, nuevo_ancho - 10, nuevo_alto - 10, fill="#F0F0F0", outline="black", width=1)
    canvas_planta.create_text(x_planta_origen + 10, y_planta_origen + 15, text="LEYENDA DE SOLUCIONES", anchor=tk.W, font=fuente_titulo, fill="black")
    
    # Símbolo 1: CSN (Azul)
    y_item = y_planta_origen + 40
    canvas_planta.create_oval(x_planta_origen + 15 - 4, y_item - 4, x_planta_origen + 15 + 4, y_item + 4, fill="blue", outline="black")
    canvas_planta.create_text(x_planta_origen + 30, y_item, text="Solución CSN", anchor=tk.W, font=fuente_texto, fill="black")
    
    # Símbolo 2: Agencia Base (Verde)
    y_item += espacio_items
    canvas_planta.create_oval(x_planta_origen + 15 - 4, y_item - 4, x_planta_origen + 15 + 4, y_item + 4, fill="green", outline="black")
    canvas_planta.create_text(x_planta_origen + 30, y_item, text=f"Agencia Base ({agenciabase})", anchor=tk.W, font=fuente_texto, fill="black")

    # Símbolo 3: Evento Percibido (Rojo)
    y_item += espacio_items
    canvas_planta.create_oval(x_planta_origen + 15 - 4, y_item - 4, x_planta_origen + 15 + 4, y_item + 4, fill="red", outline="black")
    canvas_planta.create_text(x_planta_origen + 30, y_item, text="Evento Percibido", anchor=tk.W, font=fuente_texto, fill="black")

    # Símbolo 4: Soluciones Superpuestas (Aro Magenta + Centro Agencia)
    y_item += espacio_items
    canvas_planta.create_oval(x_planta_origen + 15 - 7, y_item - 7, x_planta_origen + 15 + 7, y_item + 7, outline="magenta", width=2)
    canvas_planta.create_oval(x_planta_origen + 15 - 4, y_item - 4, x_planta_origen + 15 + 4, y_item + 4, fill="green", outline="black")
    canvas_planta.create_text(x_planta_origen + 30, y_item, text="Soluciones Superpuestas", anchor=tk.W, font=fuente_texto, fill="magenta")

    return canvas, canvas_planta, percibidos, total_eventos


def guarda_canvas_png(canvas, nombre_archivo_imagen):
    """
    Guarda el contenido de un canvas de Tkinter como un archivo PNG.
    """
    try:
        # Crea un archivo Postscript (vectorial) a partir del canvas
        canvas.postscript(file=nombre_archivo_imagen + '.ps', colormode='color')
        
        # Abre el archivo Postscript con Pillow
        img = Image.open(nombre_archivo_imagen + '.ps')
        
        # Guarda la imagen en formato PNG
        img.save(nombre_archivo_imagen)
        
        # Opcional: elimina el archivo Postscript temporal
        import os
        os.remove(nombre_archivo_imagen + '.ps')
        
        print(f"Canvas guardado con éxito como {nombre_archivo_imagen}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return    

def mostrar_json_en_popup(ruta_archivo, nombre, percibidos, total_eventos, fuente):
    """
    Lee un archivo JSON y muestra su contenido en una ventana pop-up con scroll.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            # Carga el contenido del archivo JSON
            contenido_json = json.load(archivo)
            # Formatea el JSON para una mejor visualización (indentación)
            texto_formateado = json.dumps(contenido_json, indent=4)
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"El archivo '{ruta_archivo}' no se encontró.")
        return
    except json.JSONDecodeError:
        tk.messagebox.showerror("Error", "El archivo no es un JSON válido.")
        return
    except Exception as e:
        tk.messagebox.showerror("Error", f"Ocurrió un error: {e}")
        return

    # Crea una ventana de nivel superior (el pop-up) que muestra el contenido del archivo que se esta ploteando
    archivo_popup = tk.Toplevel()
    if fuente == "eventquery":
        archivo_popup.title(nombre + ' ( fuente ' + fuente + ' - ' + str(percibidos) + ' percibidos de ' + str(total_eventos) + ' eventos ploteados)')
    else:
        archivo_popup.title(nombre + ' ( fuente ' + fuente + ' - ' + str(total_eventos) + ' eventos ploteados)')
        
    archivo_popup.geometry("700x400") # Puedes ajustar el tamaño inicial de la ventana

    # Crea un widget ScrolledText (combina un widget Text y una Scrollbar)
    campo_texto = scrolledtext.ScrolledText(archivo_popup, wrap=tk.WORD, font=("Consolas", 10))
    campo_texto.pack(expand=True, fill="both")

    # Inserta el texto formateado en el widget
    campo_texto.insert(tk.INSERT, texto_formateado)
    campo_texto.config(state=tk.DISABLED) # Evita que el usuario edite el texto
    return

# Diccionario con perfiles de seisan
# min y max en X corresponden a longitudes
# min y  max en Y corresponden a profundidades
perfiles_seisan = {
    "Perf_18.5_-74.280000_-66.500000_250_sm.png" : {
        "minX" : -74.280000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_19.0_-73.700000_-66.500000_250_sm.png" : {
        "minX" : -73.700000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_20.0_-73.120000_-66.500000_250_sm.png" : {
        "minX" : -73.120000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_21.0_-73.920000_-66.500000_250_sm.png" : {
        "minX" : -73.920000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_22.0_-72.960000_-66.500000_250_sm.png" : {
        "minX" : -72.960000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_23.0_-73.060000_-66.500000_250_sm.png" : {
        "minX" : -73.060000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_24.0_-73.120000_-66.500000_250_sm.png" : {
        "minX" : -73.120000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_25.0_-73.140000_-66.500000_250_sm.png" : {
        "minX" : -73.140000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_26.0_-73.260000_-66.500000_250_sm.png" : {
        "minX" : -73.260000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_27.0_-73.420000_-66.500000_250_sm.png" : {
        "minX" : -73.420000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_28.0_-73.640000_-66.500000_250_sm.png" : {
        "minX" : -73.640000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_29.0_-73.900000_-66.500000_250_sm.png" : {
        "minX" : -73.900000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_30.0_-74.100000_-66.500000_250_sm.png" : {
        "minX" : -74.100000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_31.0_-74.240000_-66.500000_250_sm.png" : {
        "minX" : -74.240000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_32.0_-74.420000_-66.500000_250_sm.png" : {
        "minX" : -74.420000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_33.0_-74.640000_-66.500000_250_sm.png" : {
        "minX" : -74.640000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_34.0_-75.000000_-66.500000_250_sm.png" : {
        "minX" : -75.000000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_35.0_-75.440000_-66.500000_250_sm.png" : {
        "minX" : -75.440000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_36.0_-75.900000_-66.500000_250_sm.png" : {
        "minX" : -75.900000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_37.0_-76.200000_-66.500000_250_sm.png" : {
        "minX" : -76.200000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_38.0_-76.420000_-66.500000_250_sm.png" : {
        "minX" : -76.420000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_39.0_-76.660000_-66.500000_250_sm.png" : {
        "minX" : -76.660000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_40.0_-76.840000_-66.500000_250_sm.png" : {
        "minX" : -76.840000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_41.0_-77.020000_-66.500000_250_sm.png" : {
        "minX" : -77.020000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_42.0_-77.240000_-66.500000_250_sm.png" : {
        "minX" : -77.240000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_43.0_-77.300000_-66.500000_250_sm.png" : {
        "minX" : -77.300000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_44.0_-77.380000_-66.500000_250_sm.png" : {
        "minX" : -77.380000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "Perf_45.0_-77.380000_-66.500000_250_sm.png" : {
        "minX" : -77.380000,
        "maxX" : -66.500000,
        "minY" : -250,
        "maxY" : 15
    },
    "sin_perfil_norte.jpg" : {
        "minX" : -75.0,#da lo mismo los valores ya que no se plotearan (-75.0_-66.0_-22.0_-14.0 planta)
        "maxX" : -66.0,
        "minY" : -250,
        "maxY" : 15
    },
    "sin_perfil_sur1.jpg" : {
        "minX" : -80.0,#da lo mismo los valores ya que no se plotearan (-80.0_-57.0_-56.0_-44.0.png planta)
        "maxX" : -57.0,
        "minY" : -250,
        "maxY" : 15
    },
    "sin_perfil_sur2.jpg" : {
        "minX" : -79.0,#da lo mismo los valores ya que no se plotearan (-79.0_-53.0_-65.0_-55.0.png planta)
        "maxX" : -53.0,
        "minY" : -250,
        "maxY" : 15
    },
}

# Diccionario con mapas planta perfiles segun nombre de archivo .png de harz
# min y max en X corresponden a longitudes
# min y max en Y corresponden a latitudes
plantas = {
    "-74.0_-65.0_-24.0_-16.0.png" : {
        "minX" : -74.0,
        "maxX" : -65.0,
        "minY" : -24.0,
        "maxY" : -16.0
    },
    "-74.0_-65.0_-28.0_-20.0.png" : {
        "minX" : -74.0,
        "maxX" : -65.0,
        "minY" : -28.0,
        "maxY" : -20.0
    },
    "-76.0_-67.0_-31.0_-24.0.png" : {
        "minX" : -76.0,
        "maxX" : -67.0,
        "minY" : -31.0,
        "maxY" : -24.0
    },
    "-76.0_-67.0_-36.0_-28.0.png" : {
        "minX" : -76.0,
        "maxX" : -67.0,
        "minY" : -36.0,
        "maxY" : -28.0
    },
    "-77.0_-68.0_-40.0_-32.0.png" : {
        "minX" : -77.0,
        "maxX" : -68.0,
        "minY" : -40.0,
        "maxY" : -32.0
    },
    "-80.0_-68.0_-44.0_-36.0.png" : {
        "minX" : -80.0,
        "maxX" : -68.0,
        "minY" : -44.0,
        "maxY" : -36.0
    },
    "-80.0_-68.0_-47.0_-39.0.png" : {
        "minX" : -80.0,
        "maxX" : -68.0,
        "minY" : -47.0,
        "maxY" : -39.0
    },
    "-80.0_-68.0_-48.0_-41.0.png" : {
        "minX" : -80.0,
        "maxX" : -68.0,
        "minY" : -48.0,
        "maxY" : -41.0
    },
    "-80.0_-68.0_-51.0_-45.0.png" : {
        "minX" : -80.0,
        "maxX" : -68.0,
        "minY" : -51.0,
        "maxY" : -45.0
    },
    "-79.0_-63.0_-55.0_-49.0.png" : {
        "minX" : -79.0,
        "maxX" : -63.0,
        "minY" : -55.0,
        "maxY" : -49.0
    },
    "-78.0_-63.0_-60.0_-54.0.png" : {
        "minX" : -78.0,
        "maxX" : -63.0,
        "minY" : -60.0,
        "maxY" : -54.0
    },
    "-75.0_-66.0_-22.0_-14.0.png" : {
        "minX" : -75.0,
        "maxX" : -66.0,
        "minY" : -22.0,
        "maxY" : -14.0
    },
    "-80.0_-57.0_-56.0_-44.0.png" : {
        "minX" : -80.0,
        "maxX" : -57.0,
        "minY" : -56.0,
        "maxY" : -44.0
    },
    "-79.0_-53.0_-65.0_-55.0.png" : {
        "minX" : -79.0,
        "maxX" : -53.0,
        "minY" : -65.0,
        "maxY" : -55.0
    },
}

# Diccionario que define con que plotear segun el archivo de datos .json con los mapas de planta de harz
plotear = {
    "file_a.json" : {
        "archivo" : "sin_perfil_norte",
        "perfil"  : "sin_perfil_norte.jpg",
        "planta"  : "-75.0_-66.0_-22.0_-14.0.png"
    },
    "file_b1.json" : {
        "archivo" : "Perfil18",
        "perfil"  : "Perf_18.5_-74.280000_-66.500000_250_sm.png",
        "planta"  : "-74.0_-65.0_-24.0_-16.0.png"
    },
    "file_b2.json" : {
        "archivo" : "Perfil20",
        "perfil"  : "Perf_20.0_-73.120000_-66.500000_250_sm.png",
        "planta"  : "-74.0_-65.0_-24.0_-16.0.png"
    },
    "file_c.json" : {
        "archivo" : "Perfil24",
        "perfil"  : "Perf_24.0_-73.120000_-66.500000_250_sm.png",
        "planta"  : "-74.0_-65.0_-28.0_-20.0.png"
    },
    "file_d.json" : {
        "archivo" : "Perfil28",
        "perfil"  : "Perf_28.0_-73.640000_-66.500000_250_sm.png",
        "planta"  : "-76.0_-67.0_-31.0_-24.0.png"
    },
    "file_e.json" : {
        "archivo" : "Perfil33",
        "perfil"  : "Perf_33.0_-74.640000_-66.500000_250_sm.png",
        "planta"  : "-76.0_-67.0_-36.0_-28.0.png"
    },
    "file_f.json" : {
        "archivo" : "Perfil37",
        "perfil"  : "Perf_37.0_-76.200000_-66.500000_250_sm.png",
        "planta"  : "-77.0_-68.0_-40.0_-32.0.png"
    },
    "file_g.json" : {
        "archivo" : "Perfil41",
        "perfil"  : "Perf_41.0_-77.020000_-66.500000_250_sm.png",
        "planta"  : "-80.0_-68.0_-44.0_-36.0.png"
    },
    "file_h.json" : {
        "archivo" : "Perfil43",
        "perfil"  : "Perf_43.0_-77.300000_-66.500000_250_sm.png",
        "planta"  : "-80.0_-68.0_-47.0_-39.0.png"
    },
    "file_i.json" : {
        "archivo" : "Perfil45",
        "perfil"  : "Perf_45.0_-77.380000_-66.500000_250_sm.png",
        "planta"  : "-80.0_-68.0_-48.0_-41.0.png"
    },
    "file_j.json" : {
        "archivo" : "sin_perfil_sur1",
        "perfil"  : "sin_perfil_sur1.jpg",
        "planta"  : "-80.0_-57.0_-56.0_-44.0.png"
    },
    "file_k.json" : {
        "archivo" : "sin_perfil_sur2",
        "perfil"  : "sin_perfil_sur2.jpg",
        "planta"  : "-79.0_-53.0_-65.0_-55.0.png"
    },
}

"""
# Cargar en una lista los nombres de los archivos json que se generan en la carpeta donde se ejecuta el script
lista = [file for file in os.listdir() if file[-4:] == "json"]
listajson=sorted(lista)
largo=len(listajson)
print('lista archivos json')
print(listajson)
#print('largo lista:',largo)
"""

# argumento enviado al ejecutar el script para plotear (archivo .json)
archivo=sys.argv[1]
fuente=sys.argv[2]
agenciabase=sys.argv[3]
print('agencia base:', agenciabase)
percibidos=0

# resolucion para cada imagen y para el canvas
nuevo_ancho = 800
nuevo_alto = 800
ventana, canvas, canvas_planta=crear_canvas(nuevo_ancho, nuevo_alto)

perfil_elegido=plotear[archivo]["perfil"]
planta_elegido=plotear[archivo]["planta"]
archivo_elegido=archivo

try:
    # Mapas perfiles (ruta al mapa del perfil a utilizar usando os.path.join)
    imagen_perfil_path = os.path.join(path_perfil, "sin_margen", perfil_elegido)
    
    # Mapas planta (ruta al mapa de planta a utilizar)
    imagen_planta_path = os.path.join(path_planta, planta_elegido)

except FileNotFoundError:
    print("Error: No se encontró la imagen.")
    exit()
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    exit()

"""
try:
    
    # Mapas perfiles (ruta al mapa del perfil a utilizar)
    imagen_perfil_path = path_perfil+"/sin_margen/"+perfil_elegido # ruta a la imagen
    
    # Mapas planta (ruta al mapa de planta a utilizar)
    imagen_planta_path = path_planta+"/"+planta_elegido  # ruta a la imagen

except FileNotFoundError:
    print("Error: No se encontró la imagen.")
    exit()
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    exit()
"""

# Redimensionar la imagen y obtener la versión compatible con Tkinter
imagen_tk = redimensionar_imagen(imagen_perfil_path, nuevo_ancho, nuevo_alto)
imagen_tk_planta = redimensionar_imagen(imagen_planta_path, nuevo_ancho, nuevo_alto)

# Mostrar la imagen en el canvas
mostrar_imagen_en_canvas(canvas, imagen_tk)
canvas.create_text(250, nuevo_alto-50, text=perfil_elegido[:-4], fill="black", font=("Arial", 16))
canvas.create_text(100, 20, text='Ploteando '+ archivo_elegido, fill="blue", font=("Arial", 12))
mostrar_imagen_en_canvas(canvas_planta, imagen_tk_planta)
canvas_planta.create_text(165, nuevo_alto-50, text=planta_elegido[:-4], fill="black", font=("Arial", 16))

#canvas.create_text(250, 150, text=archivo_elegido, fill="black", font=("Arial", 12))
canvas, canvas_planta, percibidos, total_eventos = ploteando(archivo_elegido, perfil_elegido, planta_elegido, fuente, percibidos, agenciabase)
#if fuente=="eventquery":
#    print('Percibidos:', percibidos)

#guarda_canvas_png(canvas, archivo_elegido[:8]+"_perfil")
#guarda_canvas_png(canvas_planta, archivo_elegido[:8]+"planta")

#guarda_canvas_png(canvas)
#guarda_canvas_png(canvas_planta)

mostrar_json_en_popup(path_ejecucion+'/'+archivo_elegido, archivo_elegido, percibidos, total_eventos, fuente)

# Iniciar el bucle principal de Tkinter
#time.sleep(5)
ventana.mainloop()

#valor_a_devolver = mostrar_json_en_popup(ruta_archivo, nombre, percibidos, total_eventos)
#sys.exit(valor_a_devolver)
