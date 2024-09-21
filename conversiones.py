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

def main():
    # Entrada de Individuos en formato binario separado por comas
    indBin = input('Ingrese individuos binarios separados por comas>>> ')

    # Obteniendo la Función de activación
    fnAdap = input('ingrese la función de adaptación: f(x)= ')

    # Obteniendo el Mínimo y Máximo de la función
    minMax = input('ingrese el máximo y el mínimo separados por comas>>> ')

    # Eliminando posibles espacios en blanco entre cada valor
    indSnEsp = indBin.replace(' ', '')
    fnAdapSnEsp = fnAdap.replace(' ', '')
    minMaxSnEsp = minMax.replace(' ', '')

    # Creando listas de los datos sin espacios (Parametro para separar; las comas)
    lstBinaria = indSnEsp.split(',')
    lstMinMax = [int(i) for i in minMaxSnEsp.split(',')]  # Conversión a entero

    # Obteniendo 'L'
    l = len(lstBinaria[0])

    valida_longitud(lstBinaria, l)

    # Comprobando Máximos y mínimos, siempre en la posición '0' debe ir el máximo
    if lstMinMax[0] < lstMinMax[1]:
        temp = lstMinMax[0]
        lstMinMax[0] = lstMinMax[1]
        lstMinMax[1] = temp

    # Imprimiendo el resultado de la conversión
    decimales = convercion_decimal(lstBinaria)
    print('\n' + '>>>>>Los individuos en decimal son:', decimales)

    # Imprimimos el valor real de los individuos
    reales = convercion_real(decimales, lstMinMax, l)
    print('\n' + '>>>>>Los Valores reales son:', reales)

    # Imprime los valores de adaptación
    adaptados, adaptacion = convercion_adaptado(reales, fnAdapSnEsp, lstMinMax)
    print('\n' + '>>>>>Los valores adaptados son:', adaptados)
    print('\n' + '>>>>>El valor que los individuos deben superar es:', adaptacion)

    # Obtenemos e imprimimos la Selección ruleta
    ruleta = seleccion_ruleta(adaptados)
    print('\n' + '>>>>>Ruleta:', ruleta, '\n')

    # Solicitamos al usuario el % de cruces que quiere tener en el algoritmo
    porcentajeCruce =  int(input("Qué porcentaje de cruce quieres manejar"))

    # Calculamos con una regla de 3 el número de cruces que corresponde con el porcentaje establecido
    noCruces = round((porcentajeCruce * len(lstBinaria)) / 100)  # >>> (% de Cruce x total de individuos) / 100%

    # Pedimos que elijan un tipo de cruce
    tipo_cruce = int(input("Qué tipo de cruce deseas hacer? 1 = Cruce de Un Punto | 2 = Cruce de Dos Puntos | 3 = Cruce Uniforme" + "\n" + ">>>"))
    switch_cruce = {1:cruce_unpunto, 2:cruce_dosPuntos, 3:cruce_uniforme}

    # Pedimos que elijan un tipo de mutación
    tipo_mutacion = int(input("Qué tipo de mutación deseas utilizar? 1 = Mutación Simple" + "\n" + ">>>"))
    switch_mutacion = {1: mutacion_simple}

    # Solicitamos al usuario el % de mutación que quiere tener en el algoritmo
    porcentaje_mutacion = int(input("Qué porcentaje de mutación quieres manejar >>> "))

    # Calculamos con una regla de 3 el número de individuos a mutar
    num_mutaciones = round((porcentaje_mutacion * len(lstBinaria)) / 100)  # >>> (% de mutación x total de individuos) / 100%

    # Usar get() con una función por defecto si 'tipo_cruce' no exist
    funcion_cruce = switch_cruce.get(tipo_cruce, lambda *args: "Opción no válida")

    # Ejecutar la función seleccionada con los parámetros
    lstBinaria = funcion_cruce(lstBinaria, noCruces, l)

    funcion_mutacion = switch_mutacion.get(tipo_mutacion, lambda *args: "Opción no válida")
    lstBinaria = funcion_mutacion(lstBinaria, num_mutaciones, l)

    total_adaptados = encontrar_mejores(lstBinaria, adaptacion)

    print(f"Se encontraron {len(total_adaptados)} individuos adaptados")
    print(total_adaptados)

if __name__ == "__main__":
    main()