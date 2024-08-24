import math
def f(x):

    x_radians = math.radians(x) # Convertir grados a radianes si es necesario
    return 3* x + 2* x + 1# Usar x directamente si está en radianes

# Solicitar al usuario los valores mínimo y máximo en grados
x_min = float(input("Introduce el valor mínimo de x (en grados): "))
x_max = float(input("Introduce el valor máximo de x (en grados): "))

# Calcular f(x) para los valores mínimo y máximo en grados
resultado_min = f(x_min)
resultado_max = f(x_max)

print(f"f({x_min}°) = {resultado_min}")
print(f"f({x_max}°) = {resultado_max}")

# Lista de números binarios
binarios = ["010111", "1101", "1000", "1110"]

# Lista para almacenar los resultados decimales
decimales = []

# Convertir cada número binario a decimal
for binario in binarios:
    decimal = int(binario, 2)
    decimales.append(decimal)

# Imprimir los resultados decimales y calcular el resultado adicional para cada uno
for binario, decimal in zip(binarios, decimales):
    print(f"El valor binario {binario} es {decimal} en decimal.")

    # Calcular el resultado adicional para cada decimal0
    resultado_adicional = x_min + decimal  * ((x_max - x_min) / (2**6 - 1))
    print(f"Resultado adicional para el decimal {decimal}: {resultado_adicional}")