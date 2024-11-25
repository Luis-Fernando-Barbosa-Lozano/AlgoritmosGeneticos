from flask import Flask, render_template, request, jsonify
import random
import math
import re

app = Flask(__name__)

# Funciones de tu algoritmo genético (reutilizadas del código proporcionado)
def generar_individuos_aleatorios(num_individuos, longitud):
    return [''.join(random.choice('01') for _ in range(longitud)) for _ in range(num_individuos)]

def valida_longitud(lstBinaria, l):
    for val in lstBinaria:
        if len(val) != l:
            raise ValueError(f'El individuo {val} no cumple con la longitud del primer elemento')

def convercion_decimal(lst_binaria):
    return [int(str(ind), 2) for ind in lst_binaria]

def convercion_real(lstDecimal, lstMinMax, l):
    return [
        round(lstMinMax[1] + vCad * ((lstMinMax[0] - lstMinMax[1]) / ((2**l) - 1)), 3)
        for vCad in lstDecimal
    ]

def encontrar_mejores(lst_binaria, valor_adaptacion):
    return [elem for elem in lst_binaria if int(elem, 2) >= valor_adaptacion]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.json
        longitud_binaria = int(data['longitud_binaria'])
        min_max = [int(x) for x in data['min_max'].split(',')]
        porcentaje_cruce = float(data['porcentaje_cruce']) / 100
        tipo_cruce = int(data['tipo_cruce'])
        porcentaje_mutacion = float(data['porcentaje_mutacion']) / 100
        funcion_adaptacion = data['funcion_adaptacion']

        # Validaciones básicas
        if len(min_max) != 2 or min_max[0] == min_max[1]:
            raise ValueError("Rango Min y Max inválido.")
        if not (0 <= porcentaje_cruce <= 1):
            raise ValueError("Porcentaje de Cruce debe estar entre 0% y 100%.")
        if not (0 <= porcentaje_mutacion <= 1):
            raise ValueError("Porcentaje de Mutación debe estar entre 0% y 100%.")
        if tipo_cruce not in [1, 2, 3]:
            raise ValueError("Tipo de Cruce inválido. Usa 1, 2 o 3.")

        # Aseguramos que los límites estén ordenados
        if min_max[0] < min_max[1]:
            min_max[0], min_max[1] = min_max[1], min_max[0]

        # Generación de individuos iniciales
        lst_binaria = generar_individuos_aleatorios(500, longitud_binaria)
        valida_longitud(lst_binaria, longitud_binaria)

        porcentaje_convergencia = 0
        iteracion = 1

        while porcentaje_convergencia < 70:
            # Conversión y evaluación
            decimales = convercion_decimal(lst_binaria)
            reales = convercion_real(decimales, min_max, longitud_binaria)

            # Proceso de cruce según tipo seleccionado
            if tipo_cruce == 1:
                # Implementar lógica para cruce de un punto
                pass
            elif tipo_cruce == 2:
                # Implementar lógica para cruce de dos puntos
                pass
            elif tipo_cruce == 3:
                # Implementar lógica para cruce uniforme
                pass

            # Proceso de mutación basado en porcentaje_mutacion
            # (Añadir lógica según diseño del algoritmo)

            # Evaluación de adaptados
            total_adaptados = encontrar_mejores(lst_binaria, sum(reales) / len(reales))
            porcentaje_convergencia = (len(total_adaptados) / len(lst_binaria)) * 100
            iteracion += 1

        return jsonify({
            'message': f"Convergencia alcanzada: {porcentaje_convergencia:.2f}%",
            'total_adaptados': len(total_adaptados)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
