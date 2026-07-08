#!/bin/bash
SCRIPTS="/home/hriquelmez/Desarrollo"
PROYECTO="revisaapis"

# saca comentario cuando se desee hacer la consulta a las apis
python3 $SCRIPTS/$PROYECTO/consultaapi.py $1 $2 $3

# BUCLE DE VALIDACIÓN: Asegura que el archivo tenga extensión .csv y realmente exista
while true; do
    read -p "Archivo .csv fuente eventquery: " archivo1
    
    # Verifica si el archivo existe
    if [ ! -f "$archivo1" ]; then
        echo -e "El archivo '$archivo1' no existe. Por favor, ingresa un archivo válido.\n"
        continue
    fi

    # Verificar si la extensión es estrictamente .csv (ignora mayúsculas/minúsculas)
    if [[ "$archivo1" == *.csv || "$archivo1" == *.CSV ]]; then
        break
    else
        echo -e "Error: El archivo debe ser obligatoriamente un formato .csv de eventquery.\n"
    fi
done

# Continuación normal del script si pasa la validación
cp "$archivo1" "origen_$archivo1"

archivo1aux=${archivo1:0:$((${#archivo1}-4))}
archivo1dat=$archivo1aux'.dat'

python3 $SCRIPTS/$PROYECTO/proc_query_harz_2.py "$archivo1" "$archivo1dat"

echo -e "\n***** Se consolida consultas api *****"
# copia archivo csv del eventquery oredenado con un nombre similar a las otras consultas
#cp new_2_$archivo1 consultaapi_CSN.csv
#agenciabase=$(python3 /home/hriquelmez/Revision_Local/revisaapi.py "new_2_$archivo1")
agenciabase=$(python3 $SCRIPTS/$PROYECTO/revisaapi.py "new_2_$archivo1")
agenciabase=$(echo "$agenciabase" | xargs)

# [Opcional] Un respaldo por si la ejecución fallara y volviera vacía
if [ -z "$agenciabase" ]; then
    agenciabase="EMSC"
fi

echo -e "Agencia base:" $agenciabase
echo -e "\n¿Que datos desea procesar para plotear?"
echo -e "1-Datos eventquery"
echo -e "2-Datos consultaapi EMSC"
echo -e "3-Datos consulta USGS"
echo -e "4-Datos consultaapi GFZ"
echo -e "5-Fuera de rango CSN"
echo -e "6-Fuera de rango (individual)"
echo -e "7-Fuera de rango (todos)"
echo -e "8-Todos"
respuesta="6"
while [ $respuesta != "1" -o $respuesta != "2" -o $respuesta != "3" -o $respuesta != "4" -o $respuesta != "5" -o $respuesta != "6" -o $respuesta != "7" ]
do
    read -p "Ingrese opción : " -n1 respuesta
    #if [ $respuesta = "1" -o $respuesta = "2" ]
    if [ $respuesta = "1" -o $respuesta = "2" -o $respuesta != "3" -o $respuesta != "4" -o $respuesta != "5" -o $respuesta != "6" -o $respuesta != "7" ]
    then
        if [ $respuesta = "1" ]
        then
            echo -e "\n***** Procesando datos extraidos desde eventquery CSN *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="eventquery"
            # se mantienen llamando a este archivo con estructura diferente para que al plotear se mantenga
            # diferenciando eventos percibidos
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py new_2_$archivo1 $fuente
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py consultaapi_CSN.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py consultaapi_CSN.csv $fuente
            break
        fi
        if [ $respuesta = "2" ]
        then
            echo -e "\n***** Procesando datos extraidos desde EMSC *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="EMSC"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py consultaapi_EMSC.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py consultaapi_EMSC.csv $fuente
            break
        fi
        if [ $respuesta = "3" ]
        then
            echo -e "\n***** Procesando datos extraidos desde USGS *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="USGS"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py  consultaapi_NEIC.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py  consultaapi_NEIC.csv $fuente
            break
        fi
        if [ $respuesta = "4" ]
        then
            echo -e "\n***** Procesando datos extraidos desde GFZ *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="GFZ"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py consultaapi_NEIC.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py consultaapi_NEIC.csv $fuente
            break
        fi
        if [ $respuesta = "5" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos para CSN *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangosCSN"
            #python3 /home/hriquelmez/Revision_Local/solocsnapi.py
            python3 $SCRIPTS/$PROYECTO/solocsnapi.py
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrangofull.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py listaoutrangofull.csv $fuente
            break
        fi
        if [ $respuesta = "6" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangos"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrango.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py listaoutrango.csv $fuente
            break
        fi
        if [ $respuesta = "7" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos de todas las agencias *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangosfull"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrangofull.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py listaoutrangofull.csv $fuente
            break
        fi
        if [ $respuesta = "8" ]
        then
            echo -e "\n***** Procesando datos extraidos desde todas las agencias *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="todas"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaapifinal.csv $fuente
            python3 $SCRIPTS/$PROYECTO/generajsonapi.py listaapifinal.csv $fuente
            break
        fi
    else
        echo -e "\n¡¡¡ Ingrese opcion valida !!!\n"
    fi
done
#rm $1
#rm $2
read -p "¿Desea plotear resultados? S/N : " -n1 respuesta 
if [ $respuesta = "S" -o $respuesta = "s" ]
then

    echo -e "\n***** Se mostrarán mapas de perfil y planta *****"
    #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
    ls file*.json > listadojson.txt
    while IFS= read -r linea
    do
        #python3 /home/hriquelmez/Revision_Local/plotearapi.py $linea $fuente $agenciabase
        python3 $SCRIPTS/$PROYECTO/plotearapi.py "$linea" "$fuente" "$agenciabase"
        #python3 $SCRIPTS/$PROYECTO/plotearapi.py $linea $fuente $agenciabase
    done < listadojson.txt
    rm listadojson.txt
    if [ $fuente = "eventquery" ]
    then
        # Inicializar la variable en el script principal
        percibidos=0

        # Usar la sustitución de procesos para alimentar el bucle desde 'tail'
        while IFS= read -r linea
        do
            # El bucle se ejecuta en el shell principal
            # Incrementar el contador
            ((percibidos++))
        done < <(tail -n +2 "percibidos.txt")
        echo -e "Eventos ploteados, de los cuales $percibidos fueron reportados como percibidos"
    else
        echo -e "Se plotearon eventos"
    fi
else
    echo -e "\n¡¡¡ Hasta pronto !!!"
fi
if [[ ! -f "$archivo1" ]]; then
    mv origen_$archivo1 $archivo1
fi
