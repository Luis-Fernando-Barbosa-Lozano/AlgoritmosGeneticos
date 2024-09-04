import math
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
    adaptacion = expr = expr.replace('x', str(lstMinMax[0]))

    return valAdap, adaptacion

def metodo_ruleta(valAdap):
    # Método de ruleta (ordenar de mayor a menor)
    valAdap.sort(reverse=True)  # Ordenar la lista de mayor a menor
    return valAdap

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

    # Imprime el método de ruleta
    print('\n' + '>>>>>Ruleta:', metodo_ruleta(adaptados), '\n')

    # Solicitamos al usuario el % de cruces que quiere tener en el algoritmo y especificamos que usaremos un float
    porcentajeCruce: float = input("Qué porcentaje de cruce quieres manejar")

    # Calculamos con una regla de 3 el número de cruces que corresponde con el porcentaje establecido
    noCruces = round((porcentajeCruce * len(lstBinaria)) / 100)  # >>> (% de Cruce x total de individuos) / 100%

    # Pedimos que elijan un tipo de cruce
    tipoCruce = input("Qué tipo de cruce deseas hacer? 1= Cruce de un punto | 2= Cruce de dos puntos")

if __name__ == "__main__":
    main()