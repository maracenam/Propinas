import csv

def leer_csv(ruta_archivo):
    filas_csv = []
    with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.reader(csvfile)
        for fila in lector_csv:
            filas_csv.append(fila)
    return filas_csv

def calcular_propinas(filas_csv, propinas_totales):
    a = 2
    b = 0

    horas_totales = 0
    minutos_totales = 0
    horas_por_nombre = {}
    total_horas_trabajadas = 0  
    total_minutos_trabajados = 0

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
        propina_redondeada = round(propina / 10) * 10
        propinas_por_nombre[nombre] = propina_redondeada
        print(f"{nombre} ha trabajado {horas}:{minutos:02d} horas y recibirá una propina de {propina_redondeada}")

    print(f"Total de horas trabajadas: {total_horas_trabajadas}:{total_minutos_trabajados:02d}")

    return propinas_por_nombre, horas_por_nombre

def ingresar_dinero_efectivo():
    print("Ingrese la cantidad de dinero en efectivo que tiene:")
    billetes_20000 = int(input("Billetes de 20000: "))
    billetes_10000 = int(input("Billetes de 10000: "))
    billetes_5000 = int(input("Billetes de 5000: "))
    billetes_2000 = int(input("Billetes de 2000: "))
    billetes_1000 = int(input("Billetes de 1000: "))
    monedas_500 = int(input("Monedas de 500: "))
    monedas_100 = int(input("Monedas de 100: "))
    monedas_50 = int(input("Monedas de 50: "))
    monedas_10 = int(input("Monedas de 10: "))

    total_efectivo = (
        billetes_20000 * 20000 +
        billetes_10000 * 10000 +
        billetes_5000 * 5000 +
        billetes_2000 * 2000 +
        billetes_1000 * 1000 +
        monedas_500 * 500 +
        monedas_100 * 100 +
        monedas_50 * 50 +
        monedas_10 * 10
    )

    efectivo = {
        20000: billetes_20000,
        10000: billetes_10000,
        5000: billetes_5000,
        2000: billetes_2000,
        1000: billetes_1000,
        500: monedas_500,
        100: monedas_100,
        50: monedas_50,
        10: monedas_10
    }

    print(f"Total en efectivo: {total_efectivo}")
    return total_efectivo, efectivo    

def sencillar_dinero(faltante, restante, denominaciones):
    cambio = {}
    fuente_cambio = {}

    # Intentar encontrar la menor denominación que sea mayor que el faltante
    for denom in sorted(denominaciones):
        if restante[denom] > 0 and denom > faltante:
            cambio_posible = denom
            break
    else:
        return None, restante, None

    # Intentar sencillar el billete/moneda grande
    restante[cambio_posible] -= 1
    restante_resto = cambio_posible - faltante

    # Generar el cambio con denominaciones menores
    for denom in denominaciones:
        if denom <= restante_resto:
            cantidad = restante_resto // denom
            if cantidad > 0:
                if denom in cambio:
                    cambio[denom] += cantidad
                else:
                    cambio[denom] = cantidad
                restante_resto -= cantidad * denom

    # Asegurarse de que el cambio restante no se pierde
    if restante_resto > 0:
        if restante_resto in cambio:
            cambio[restante_resto] += 1
        else:
            cambio[restante_resto] = 1

    # Actualizar el fondo restante con el cambio dado
    for denom, cantidad in cambio.items():
        restante[denom] += cantidad
        
    # Guardar la fuente del cambio
    fuente_cambio[cambio_posible] = cambio_posible - faltante
    
    return cambio, restante, fuente_cambio

def distribuir_efectivo(propinas_por_nombre, efectivo):
    denominaciones = sorted(efectivo.keys(), reverse=True)
    distribucion = {}
    faltante_por_nombre = {}
    restante = efectivo.copy()

    for nombre, propina in propinas_por_nombre.items():
        distribucion[nombre] = {}
        faltante_por_nombre[nombre] = propina
        for denominacion in denominaciones:
            cantidad = min(propina // denominacion, restante[denominacion])
            distribucion[nombre][denominacion] = cantidad
            propina -= cantidad * denominacion
            restante[denominacion] -= cantidad
            faltante_por_nombre[nombre] = propina

        if propina > 0:
            print(f"No hay suficiente efectivo para cubrir la propina de {nombre}. Falta {propina}.")

        for nombre, faltante in faltante_por_nombre.items():
            if faltante > 0:
                cambio, restante, fuente_cambio = sencillar_dinero(faltante, restante, denominaciones)
                if cambio:
                    print(f"Para cubrir el faltante de {nombre}, sencille el dinero: {cambio} Fuente: {fuente_cambio}")
                    for denom, cantidad in cambio.items():
                        distribucion[nombre][denom] = distribucion[nombre].get(denom, 0) + cantidad
                    faltante_por_nombre[nombre] = 0

    return distribucion, faltante_por_nombre

def exportar_a_csv(nombre_archivo, tipo, propinas_por_nombre, horas_por_nombre, distribucion_efectivo, faltante_por_nombre, total_efectivo):
    with open(f'{nombre_archivo}_{tipo}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir la cabecera
        writer.writerow([
            "Nombre", "Horas trabajadas", "Propina", 
            "Billete de 20000", "Billete de 10000", "Billete de 5000", 
            "Billete de 2000", "Billete de 1000", "Moneda de 500", 
            "Moneda de 100", "Moneda de 50", "Moneda de 10", "Faltante", "Sencillar"
        ])
        # Escribir los datos de cada persona
        for nombre in propinas_por_nombre:
            horas, minutos = horas_por_nombre[nombre]
            propina = propinas_por_nombre[nombre]
            distribucion = distribucion_efectivo[nombre]
            faltante = faltante_por_nombre[nombre]
            sencillar_info = ""

            if faltante > 0:
                cambio, _, fuente_cambio = sencillar_dinero(faltante, total_efectivo, sorted(total_efectivo.keys(), reverse=True))
                if cambio:
                    sencillar_info = f"Sencillar: {cambio} Fuente: {fuente_cambio}"
                else:
                    sencillar_info = "No se puede sencillar"

            writer.writerow([
                nombre, f'{horas}:{minutos:02d}', propina,
                distribucion.get(20000, 0), distribucion.get(10000, 0), distribucion.get(5000, 0),
                distribucion.get(2000, 0), distribucion.get(1000, 0), distribucion.get(500, 0),
                distribucion.get(100, 0), distribucion.get(50, 0), distribucion.get(10, 0), faltante, sencillar_info
            ])
        # Sumar totales y añadir al final
        total_horas_trabajadas = sum(horas for horas, _ in horas_por_nombre.values())
        total_minutos_trabajados = sum(minutos for _, minutos in horas_por_nombre.values())
        total_horas_trabajadas += total_minutos_trabajados // 60
        total_minutos_trabajados %= 60
        total_propinas = sum(propinas_por_nombre.values())
        
        efectivo_restante = sum(total_efectivo[denom] * denom for denom in total_efectivo)

        writer.writerow([])
        writer.writerow(["Total de horas trabajadas", f'{total_horas_trabajadas}:{total_minutos_trabajados:02d}'])
        writer.writerow(["Total de propinas", total_propinas])
        writer.writerow(["Efectivo restante", efectivo_restante])
        
def procesar_archivo(nombre_archivo, tipo):
    filas_csv = leer_csv(nombre_archivo)
    propinas_totales = float(input(f"Ingrese el monto total de las propinas para {tipo}: "))
    total_efectivo, efectivo = ingresar_dinero_efectivo()
    propinas_por_nombre, horas_por_nombre = calcular_propinas(filas_csv, propinas_totales)
    distribucion_efectivo, faltante_por_nombre = distribuir_efectivo(propinas_por_nombre, efectivo)
    print(f"Distribución de efectivo para {tipo}: {distribucion_efectivo}")
    print(f"Efectivo Total para {tipo}: {total_efectivo}")
    exportar_a_csv("propinas", tipo, propinas_por_nombre, horas_por_nombre, distribucion_efectivo, faltante_por_nombre, efectivo)
    return distribucion_efectivo

propinas_semana = procesar_archivo("semana.csv", "semana")
propinas_finde = procesar_archivo("finde.csv", "fin de semana")