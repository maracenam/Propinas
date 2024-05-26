import csv

# Ruta al archivo CSV
def leer_csv(ruta_archivo):
        filas_csv = []
        with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
            lector_csv = csv.reader(csvfile)
            for fila in lector_csv:
                filas_csv.append(fila)
        return filas_csv

    # Obtener los valores de las celdas específicas
    

def calcular_propinas(filas_csv, propinas_totales):

    a = 2
    b = 0

    horas_totales = 0
    minutos_totales = 0
    horas_por_nombre = {}
    total_horas_trabajadas = 0  
    total_minutos_trabajados = 0

    #propinas_totales = float(input("Ingrese el monto total de las propinas: "))
    #print(f"Propinas Totales: {propinas_totales}")

    for i in range(b, len(filas_csv)):
        for j in range(a, len(filas_csv)):
            if filas_csv[j][2] == filas_csv[a][2]:
                hora_str = filas_csv[j][24]
                partes = hora_str.split(":")
                horas_totales += int(partes[0])
                minutos_totales += int(partes[1])
                
            else:
                break



        horas_totales += minutos_totales // 60
        minutos_totales %= 60

        if a < len(filas_csv):
            nombre = filas_csv[a][1]  # Nombre de la persona
            horas_por_nombre[nombre] = (horas_totales, minutos_totales) 

        #print(f"{horas_totales}:{minutos_totales:02d}", "este es la suma de horas de" , filas_csv[a][1])
        
        total_horas_trabajadas += horas_totales
        total_minutos_trabajados += minutos_totales
        
        horas_totales = 0
        minutos_totales = 0
        a = j 

        if a >= len(filas_csv):
            break



    horas_extras_por_nombre = {}
    for nombre in horas_por_nombre.keys():
        horas_extras_str = input(f"Ingrese las horas extras para {nombre} en formato HH,MM: (o '0' si no hay horas extras): ")
        if horas_extras_str == "0":
            horas_extras_por_nombre[nombre] = (0, 0)
        else:    
            horas_extras_partes = horas_extras_str.split(",")
            horas_extras_horas = int(horas_extras_partes[0])
            horas_extras_minutos = int(horas_extras_partes[1])
            horas_extras_por_nombre[nombre] = (horas_extras_horas, horas_extras_minutos)

    for nombre, (horas, minutos) in horas_por_nombre.items():
        horas_extras_horas, horas_extras_minutos = horas_extras_por_nombre.get(nombre, (0, 0))
        total_horas = horas + horas_extras_horas
        total_minutos = minutos + horas_extras_minutos
        total_horas += total_minutos // 60
        total_minutos %= 60
        horas_por_nombre[nombre] = (total_horas, total_minutos)

    total_horas_trabajadas = sum(horas for horas, _ in horas_por_nombre.values())
    total_minutos_trabajados = sum(minutos for _, minutos in horas_por_nombre.values())

    total_horas_trabajadas += total_minutos_trabajados // 60
    total_minutos_trabajados %= 60


    total_horas_decimal = total_horas_trabajadas + total_minutos_trabajados / 60
    propina_por_hora = propinas_totales / total_horas_decimal
    print(f"Propina por hora: {propina_por_hora:.2f}")

    propinas_por_nombre = {}
    for nombre, (horas, minutos) in horas_por_nombre.items():
        horas_decimal = horas + minutos / 60
        propina = propina_por_hora * horas_decimal
        propinas_por_nombre[nombre] = round(propina)
        print(f"{nombre} ha trabajado {horas}:{minutos:02d} horas y recibirá una propina de {round(propina)}")


    #for nombre, (horas, minutos) in horas_por_nombre.items():
    #    print(f"{horas}:{minutos:02d} este es la suma de horas de {nombre}")


    print(f"Total de horas trabajadas: {total_horas_trabajadas}:{total_minutos_trabajados:02d}")

    return propinas_por_nombre

def procesar_archivo(nombre_archivo, tipo):
    filas_csv = leer_csv(nombre_archivo)
    propinas_totales = float(input(f"Ingrese el monto total de las propinas para {tipo}: "))
    #print(f"Propinas Totales para {tipo}: {propinas_totales}")
    return calcular_propinas(filas_csv, propinas_totales)

propinas_semana = procesar_archivo("semana.csv", "semana")
propinas_finde = procesar_archivo("finde.csv", "fin de semana")


#print("Valor de la tercera columna de la segunda fila:", valor_1)
#print("Valor de la vigésimo quinta columna de la segunda fila:", valor_2)
