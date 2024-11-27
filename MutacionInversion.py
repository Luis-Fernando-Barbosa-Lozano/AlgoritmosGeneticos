import random


def mutacion_por_inversion(lstBinaria, num_mutaciones, longitud_binaria):
    """
    Aplica mutación por inversión a una población representada por listas binarias.

    Parámetros:
    - lstBinaria: Lista de individuos (listas binarias).
    - num_mutaciones: Número de mutaciones a aplicar.
    - longitud_binaria: Longitud de los genes de los individuos.

    Retorna:
    - La población mutada (lstBinaria).
    """
    for _ in range(num_mutaciones):
        # Seleccionar un individuo aleatorio para mutar (en este caso, una lista binaria)
        indice_individuo = random.randint(0, len(lstBinaria) - 1)
        individuo = lstBinaria[indice_individuo]

        # Elegir dos índices aleatorios para realizar la inversión
        inicio = random.randint(0, len(individuo) - 1)
        fin = random.randint(inicio + 1, len(individuo))

        # Invertir la subsecuencia de genes entre los índices seleccionados
        individuo_mutado = individuo[:inicio] + individuo[inicio:fin][::-1] + individuo[fin:]

        # Actualizar el individuo en la población usando el índice
        lstBinaria[indice_individuo] = individuo_mutado

        #print(f"Mutación por inversión aplicada. Individuo mutado: {individuo_mutado}")

    return lstBinaria
