# Selección jerárquica
import random


def seleccion_jerarquica(valAdap):
    # Ordenar los valores de adaptación de menor a mayor (como en ruleta)
    poblacion_ordenada = sorted(enumerate(valAdap), key=lambda x: x[1])

    # Calcular las probabilidades basadas en el ranking (más alto es mejor)
    total_individuos = len(poblacion_ordenada)
    probabilidades = []

    for i in range(total_individuos):
        # Se asigna mayor probabilidad a los mejores individuos
        probabilidad = (total_individuos - i) / sum(range(1, total_individuos + 1))
        probabilidades.append(probabilidad)

    # Realizar la selección según las probabilidades
    seleccionados = random.choices(poblacion_ordenada, weights=probabilidades, k=2)

    # Extraer los índices de los individuos seleccionados
    indices_seleccionados = [individuo[0] for individuo in seleccionados]

    return indices_seleccionados
