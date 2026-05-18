#!/bin/bash
SCRIPTS="/home/hriquelme/Desarrollo"
PROYECTO="revisaapis"
# sacar comentario cuando se desee hacer la consulta a las apis por ahora se tiene consultas generadas para pruebas
# en el directorio de ejecucion debe estar el .csv de la consulta de datos de eventquery
# ejemplo de ejecucion
# consultaapi.sh 2026-01-01T00:00:00 2026-01-31T23:59:59 1 # el 1 es minima magnitud
#python3 /home/hriquelmez/Revision_Local/consultaapi.py $1 $2 $3
python3 $CRIPTS/$PROYECTO/consultaapi.py $1 $2 $3
read -p "Archivo .csv fuente eventquery: " archivo1
cp $archivo1 origen_$archivo1
#read -p "Archivo .csv consultaapi EMSC : " archivo2
archivo1aux=${archivo1:0:$((${#archivo1}-4))}
archivo1dat=$archivo1aux'.dat'
#python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $archivo1 $archivo1dat
python3 $CRIPTS/$PROYECTO/proc_query_harz_2.py $archivo1 $archivo1dat
echo -e "\n***** Se consolida consultas api *****"
# copia archivo csv del eventquery oredenado con un nombre similar a las otras consultas
#cp new_2_$archivo1 consultaapi_CSN.csv
#agenciabase=$(python3 /home/hriquelmez/Revision_Local/revisaapi.py "new_2_$archivo1")
agenciabase=$(python3 $CRIPTS/$PROYECTO/revisaapi.py "new_2_$archivo1")
agenciabase=$(echo "$agenciabase" | xargs)
#echo -e $agenciabase
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
            python3 $CRIPTS/$PROYECTO/generajsonapi.py consultaapi_CSN.csv $fuente
            break
        fi
        if [ $respuesta = "2" ]
        then
            echo -e "\n***** Procesando datos extraidos desde EMSC *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="EMSC"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py consultaapi_EMSC.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py consultaapi_EMSC.csv $fuente
            break
        fi
        if [ $respuesta = "3" ]
        then
            echo -e "\n***** Procesando datos extraidos desde USGS *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="USGS"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py  consultaapi_NEIC.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py  consultaapi_NEIC.csv $fuente
            break
        fi
        if [ $respuesta = "4" ]
        then
            echo -e "\n***** Procesando datos extraidos desde GFZ *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="GFZ"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py consultaapi_NEIC.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py consultaapi_NEIC.csv $fuente
            break
        fi
        if [ $respuesta = "5" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos para CSN *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangosCSN"
            #python3 /home/hriquelmez/Revision_Local/solocsnapi.py
            python3 $CRIPTS/$PROYECTO/solocsnapi.py
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrangofull.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py listaoutrangofull.csv $fuente
            break
        fi
        if [ $respuesta = "6" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangos"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrango.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py listaoutrango.csv $fuente
            break
        fi
        if [ $respuesta = "7" ]
        then
            echo -e "\n***** Procesando datos extraidos que estan fuera de rangos definidos de todas las agencias *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="outrangosfull"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaoutrangofull.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py listaoutrangofull.csv $fuente
            break
        fi
        if [ $respuesta = "8" ]
        then
            echo -e "\n***** Procesando datos extraidos desde todas las agencias *****"
            #python3 /home/hriquelmez/Revision_Local/proc_query_harz_2.py $1 $2
            fuente="todas"
            #python3 /home/hriquelmez/Revision_Local/generajsonapi.py listaapifinal.csv $fuente
            python3 $CRIPTS/$PROYECTO/generajsonapi.py listaapifinal.csv $fuente
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
        python3 $CRIPTS/$PROYECTO/plotearapi.py $linea $fuente $agenciabase
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
