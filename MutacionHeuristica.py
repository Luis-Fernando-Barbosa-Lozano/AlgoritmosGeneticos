import random

# Función para realizar la mutación heurística 2-opt
def mutacion_heuristica(lst_binaria, total_mutacion, longitud):
    cont = 0

    while cont != total_mutacion:
        # Seleccionamos un individuo aleatorio
        indice_individuo = random.randint(0, len(lst_binaria) - 1)
        individuo = list(lst_binaria[indice_individuo])  # Convertir en lista para manipular

        # Generamos tres índices aleatorios distintos
        indices = sorted(random.sample(range(1, longitud), 3))  # Índices entre 1 y longitud - 1

        # Aplicamos la mutación heurística: invertir segmentos entre los índices
        i, j, k = indices
        nueva_ruta = (
            individuo[:i]
            + individuo[i:j + 1][::-1]
            + individuo[j:k + 1][::-1]
            + individuo[k:]
        )

        # Convertimos de nuevo a string y actualizamos la lista original
        lst_binaria[indice_individuo] = "".join(nueva_ruta)
        cont += 1

    return lst_binaria


# Ejemplo de uso
if __name__ == "__main__":
    # Lista de individuos en formato binario
    poblacion_binaria = ["1010101", "1110001", "0101010"]
    total_mutaciones = 5
    longitud_individuo = len(poblacion_binaria[0])  # Suponemos longitud fija

    print("Población inicial:", poblacion_binaria)
    nueva_poblacion = mutacion_heuristica(poblacion_binaria, total_mutaciones, longitud_individuo)
    print("Población después de mutaciones:", nueva_poblacion)


