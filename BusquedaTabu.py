import random

# Función para calcular la distancia total de una ruta (simplificado)
def calcular_distancia(ruta):
    return sum(abs(ruta[i] - ruta[i+1]) for i in range(len(ruta)-1)) + abs(ruta[-1] - ruta[0])

# Función para generar una ruta vecina (por ejemplo, intercambiar dos ciudades)
def generar_vecina(ruta):
    i, j = random.sample(range(len(ruta)), 2)
    nueva_ruta = ruta[:]
    nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
    return nueva_ruta

# Búsqueda Tabú
def busqueda_tabu(ruta_inicial, iteraciones, tabu_tamano):
    ruta_actual = ruta_inicial
    mejor_ruta = ruta_inicial
    mejor_distancia = calcular_distancia(ruta_inicial)
    lista_tabu = []

    for _ in range(iteraciones):
        # Generar soluciones vecinas
        vecinas = [generar_vecina(ruta_actual) for _ in range(10)]  # 10 vecinas generadas aleatoriamente
        vecinas = [v for v in vecinas if v not in lista_tabu]  # Evitar soluciones en la lista tabú

        if not vecinas:
            break  # Si no hay vecinas válidas, termina la búsqueda

        # Seleccionar la mejor vecina
        vecina_mejor = min(vecinas, key=calcular_distancia)
        distancia_vecina = calcular_distancia(vecina_mejor)

        # Si la vecina es mejor que la solución actual, actualizamos
        if distancia_vecina < mejor_distancia:
            mejor_ruta = vecina_mejor
            mejor_distancia = distancia_vecina

        # Actualizar la lista tabú
        lista_tabu.append(ruta_actual)
        if len(lista_tabu) > tabu_tamano:
            lista_tabu.pop(0)

        ruta_actual = vecina_mejor

    return mejor_ruta, mejor_distancia

# Función para ingresar la ruta inicial desde el teclado
def ingresar_ruta():
    ruta = input("Ingresa la ruta inicial (por ejemplo, '1 3 6 4 2 5 8 7'): ")
    ruta = list(map(int, ruta.split()))  # Convierte la entrada en una lista de enteros
    return ruta

# Función para ingresar el número de iteraciones desde el teclado
def ingresar_iteraciones():
    iteraciones = int(input("Ingresa el número de iteraciones: "))
    return iteraciones

# Función para ingresar el tamaño de la lista tabú desde el teclado
def ingresar_tabu_tamano():
    tabu_tamano = int(input("Ingresa el tamaño de la lista tabú: "))
    return tabu_tamano

# Ejecución del programa con entradas desde el teclado
def main():
    # Ingresar valores desde el teclado
    ruta_inicial = ingresar_ruta()
    iteraciones = ingresar_iteraciones()
    tabu_tamano = ingresar_tabu_tamano()

    # Ejecución de búsqueda tabú
    mejor_ruta, mejor_distancia = busqueda_tabu(ruta_inicial, iteraciones, tabu_tamano)

    # Imprimir resultados
    print("Mejor ruta encontrada:", mejor_ruta)
    print("Distancia de la mejor ruta:", mejor_distancia)

# Llamar a la función principal
if __name__ == "__main__":
    main()
