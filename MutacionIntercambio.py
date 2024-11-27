import random

# Función de mutación por intercambio
def mutacion_por_intercambio(lstBinaria, numMutaciones, l):
    for _ in range(numMutaciones):
        # Seleccionar un individuo aleatorio de la lista
        indice_individuo = random.randint(0, len(lstBinaria) - 1)
        individuo = lstBinaria[indice_individuo]  # Ya está como cadena, no necesitamos convertirlo a lista

        # Convertir el individuo a una lista de caracteres para realizar el intercambio
        individuo = list(individuo)

        # Realizar el intercambio en dos posiciones aleatorias
        i, j = random.sample(range(l), 2)  # Seleccionar dos posiciones aleatorias dentro de la longitud
        individuo[i], individuo[j] = individuo[j], individuo[i]  # Intercambiar los genes en esas posiciones

        # Reemplazar el individuo en la lista original con la nueva cadena
        lstBinaria[indice_individuo] = ''.join(individuo)

    return lstBinaria
