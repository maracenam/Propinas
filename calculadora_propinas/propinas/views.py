from django.shortcuts import render

def calcular_propinas(request):
    if request.method == 'POST':
        propinas_totales = float(request.POST['propinas_totales'])
        # Aquí va tu lógica para calcular las propinas
        # Puedes acceder a los datos ingresados por el usuario utilizando request.POST
        # Realiza los cálculos necesarios y pasa los resultados a tu template HTML
        # Por ejemplo:
        propina_por_hora = propinas_totales / 40  # Ejemplo: asumiendo 40 horas de trabajo
        return render(request, 'propinas/resultado.html', {'propina_por_hora': propina_por_hora})
    else:
        return render(request, 'propinas/calculadora.html')