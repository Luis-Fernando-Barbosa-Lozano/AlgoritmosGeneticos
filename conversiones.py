import math
import random
import re

# Validando que todos los individuos tengan la misma longitud
def valida_longitud(lstBinaria, l):
        for val in lstBinaria:
            if len(val) != l:
                raise ValueError(f'El individuo {val} no cumple con la longitud del primer elemento')

# Convirtiendo cada valor binario en decimal y guardándolo en una lista nueva
def convercion_decimal(lst_binaria):
    decimal = []
    for ind in lst_binaria:
        dec = int(str(ind), 2)
        decimal.append(dec)
    return decimal

# Convirtiendo de decimal a real
def convercion_real(lstDecimal, lstMinMax, l):
    valReal = []  # Creamos una lista para guardar el valor real de los individuos
    for vCad in lstDecimal:
        xReal = lstMinMax[1] + vCad * ((lstMinMax[0] - lstMinMax[1]) / ((2 ** l) - 1))  # Fórmula para obtener Xreal
        valReal.append(round(xReal, 3))  # Agregamos los valores reales a una lista y truncamos el resultado a 3 decimales
    return valReal

# Obtener valor Adaptado
def convercion_adaptado(valReal, fnAdaptacion, lstMinMax):
    valAdap = []

    # Definir un diccionario de funciones matemáticas disponibles para eval, devolviendo resultados en grados
    math_functions = {
        'sen': lambda x: math.sin(math.radians(x)),
        'cos': lambda x: math.degrees(math.cos(math.radians(x))),
        'tan': lambda x: math.degrees(math.tan(math.radians(x))),
        'sqrt': math.sqrt,
        'log': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e
    }

    for ind in valReal:
        # Insertar el operador de multiplicación donde sea necesario
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', fnAdaptacion)

        # Reemplaza 'x' por el valor real en la función
        expr = expr.replace('x', str(ind))  # Sustituimos X por el valor real del individuo

        # Evalúa la expresión de manera segura usando las funciones matemáticas
        resultado = eval(expr, {"__builtins__": None}, math_functions)
        valAdap.append(round(resultado, 3))

    # Calculamos el valor de adaptación en la función
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', fnAdaptacion)
    expr = expr.replace('x', str(lstMinMax[0]))
    adaptacion = eval(expr, {"__builtins__": None}, math_functions)

    return valAdap, adaptacion

# Mutación Simple
def mutacion_simple(lst_binaria, total_mutacion, l):
    cont = 0

    while cont != total_mutacion:
        # Elegir un individuo aleatorio de la lista
        indice_individuo = random.randint(0, (len(lst_binaria) - 1))
        individuo = list(lst_binaria[indice_individuo])  # Convertir el individuo a lista para modificar

        # Elegir un bit aleatorio
        bit = random.randint(0, l - 1)

        # Realizar la mutación
        if individuo[bit] == '0':
            individuo[bit] = '1'
        else:
            individuo[bit] = '0'

        # Convertir el individuo de nuevo a string y actualizar la lista original
        lst_binaria[indice_individuo] = "".join(individuo)

        cont += 1

    return lst_binaria

# Selección ruleta (ordenar de mayor a menor)
def seleccion_ruleta(valAdap):
    valAdap.sort(reverse=True)  # Ordenar la lista de mayor a menor
    return valAdap

# Selección Torneo
def seleccion_torneo(valAdap):

    # Obteniendo el número de individuos participantes
    n = random.randint(1, len(valAdap))

    torneo = random.sample(valAdap, n)

    for i in range(len(torneo)):

        ind1, ind2 = random.sample(range(len(torneo)), 2)

        if valAdap[ind1] > valAdap[ind2]:
            torneo.remove(ind2)

        else:
            torneo.remove(ind1)

    return torneo

# Algoritmo para comparar y reemplazar en la lista
def reemplazar_padres(hijo1, hijo2, padre1, padre2, lst_binaria):
    # Convertimos los hijos y padres a decimal para comparar su "fuerza"
    hijo1_val = int(hijo1, 2)
    hijo2_val = int(hijo2, 2)
    padre1_val = int(padre1, 2)
    padre2_val = int(padre2, 2)

    # Seleccionamos al hijo más fuerte y el padre más débil
    mejor_hijo_val, mejor_hijo = (hijo1_val, hijo1) if hijo1_val > hijo2_val else (hijo2_val, hijo2)
    peor_padre_val, peor_padre = (padre1_val, padre1) if padre1_val < padre2_val else (padre2_val, padre2)

    # Reemplazamos al padre más débil con el hijo más fuerte
    peor_padre_indice = lst_binaria.index(peor_padre)
    lst_binaria[peor_padre_indice] = mejor_hijo

    return lst_binaria

# Algoritmo para cruce de un punto
def cruce_unpunto(lst_binaria, cruces, l):
    cont = 0

    # Elegimos aleatoriamente un bit de corte
    bit_corte = random.randint(1, l - 1)  # El bit e corte no puede ser el primer ni el último bit

    while cont != cruces:
        padre1 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]
        padre2 = padre1

        # nos aseguramos que ambos padres sean diferentes
        while padre2 == padre1:
            padre2 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]

        # Obtenemos los hijos; inicio1 + final2 e inicio2 + final1
        hijo1 = padre1[:bit_corte] + padre2[bit_corte:]
        hijo2 = padre2[:bit_corte] + padre1[bit_corte:]

        lst_binaria = reemplazar_padres(hijo1, hijo2, padre1, padre2, lst_binaria)

        cont += 1

    return lst_binaria

# Algoritmo para cruce de dos puntos
def cruce_dosPuntos(lst_binaria, cruces, l):
    cont = 0
    corte_q, corte_b = random.sample(range(1, l - 1), 2)

    # Aseguramos que corte_b siempre sea menor que corte_q
    if corte_b > corte_q:
        corte_b, corte_q = corte_q, corte_b

    while cont != cruces:
        padre1 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]
        padre2 = padre1

        while padre2 == padre1:
            padre2 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]

        hijo1 = padre1[:corte_q] + padre2[corte_q:corte_b] + padre1[corte_b:]
        hijo2 = padre2[:corte_q] + padre1[corte_q:corte_b] + padre2[corte_b:]

        lst_binaria = reemplazar_padres(hijo1, hijo2, padre1, padre2, lst_binaria)

        cont += 1

    return lst_binaria

# Cruce Uniforme
def cruce_uniforme(lst_binaria, cruces, l):
    cont = 0
    mascara = [random.randint(0, 1) for _ in range(l)]

    while cont != cruces:

        padre1 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]
        padre2 = padre1

        while padre2 == padre1:
            padre2 = lst_binaria[random.randint(0, len(lst_binaria) - 1)]

        hijo1 = []
        hijo2 = []

        for i in range(l):
            if mascara[i] == 0:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
            else:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])

        hijo1 = ''.join(map(str, hijo1))
        hijo2 = ''.join(map(str, hijo2))
        lst_binaria = reemplazar_padres(hijo1, hijo2, padre1, padre2, lst_binaria)

        cont += 1

    return lst_binaria

def encontrar_mejores(lst_binaria, valor_adaptacion):
    mejores = [elem for elem in lst_binaria if int(elem,2) >= valor_adaptacion]

    return mejores


def generar_individuos_aleatorios(num_individuos, longitud):
    """Genera una lista de individuos binarios aleatorios."""
    individuos = [''.join(random.choice('01') for _ in range(longitud)) for _ in range(num_individuos)]
    return individuos

def main():
    # Generación de 10,000 individuos con longitud binaria especificada
    longitud_binaria = int(input("Ingrese la longitud de los individuos binarios >>> "))
    lstBinaria = generar_individuos_aleatorios(500, longitud_binaria)
    print(f"Se generaron {len(lstBinaria)} individuos aleatorios.")

    fnAdap = input('Ingrese la función de adaptación: f(x)= ')
    minMax = input('Ingrese el máximo y el mínimo separados por comas>>> ')

    fnAdapSnEsp = fnAdap.replace(' ', '')
    minMaxSnEsp = minMax.replace(' ', '')
    lstMinMax = [int(i) for i in minMaxSnEsp.split(',')]

    valida_longitud(lstBinaria, longitud_binaria)

    if lstMinMax[0] < lstMinMax[1]:
        lstMinMax[0], lstMinMax[1] = lstMinMax[1], lstMinMax[0]

    porcentaje_convergencia = 0

    while porcentaje_convergencia < 70:
        n = 1
        print("\nIteración en proceso...")
        print("generación:", n)
        # Conversión y cálculo de adaptación
        decimales = convercion_decimal(lstBinaria)
        reales = convercion_real(decimales, lstMinMax, longitud_binaria)
        adaptados, adaptacion = convercion_adaptado(reales, fnAdapSnEsp, lstMinMax)

        porcentajeCruce = int(input("Qué porcentaje de cruce quieres manejar >>> "))
        noCruces = round((porcentajeCruce * len(lstBinaria)) / 100)

        tipo_cruce = int(input("Qué tipo de cruce deseas hacer? 1 = Un Punto | 2 = Dos Puntos | 3 = Uniforme >>> "))
        switch_cruce = {1: cruce_unpunto, 2: cruce_dosPuntos, 3: cruce_uniforme}
        funcion_cruce = switch_cruce.get(tipo_cruce, lambda *args: "Opción no válida")
        lstBinaria = funcion_cruce(lstBinaria, noCruces, longitud_binaria)

        porcentaje_mutacion = int(input("Qué porcentaje de mutación quieres manejar >>> "))
        num_mutaciones = round((porcentaje_mutacion * len(lstBinaria)) / 100)

        funcion_mutacion = mutacion_simple  # Solo tienes un tipo de mutación
        lstBinaria = funcion_mutacion(lstBinaria, num_mutaciones, longitud_binaria)

        # Encontramos los mejores individuos
        total_adaptados = encontrar_mejores(lstBinaria, adaptacion)
        n += 1

        # Calculamos el porcentaje de convergencia
        porcentaje_convergencia = (len(total_adaptados) / len(lstBinaria)) * (100)
        print(f"\nConvergencia alcanzada: {porcentaje_convergencia:.2f}%")

    print(total_adaptados)

if __name__ == "__main__":
    main()
