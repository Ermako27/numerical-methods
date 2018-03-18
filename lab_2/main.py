from math_model import *

x_gap_len = 20
x_values = []
y_values = []
ar = 0.20
for i in range(x_gap_len):
    x_values.append(round(ar, 1))
    y_values.append(round(ar+0.5, 1))
    ar += 0.5


# печать матрицы
print('Y / X', end=' ')
for elem in x_values:
    print('{:7.1f}'.format(elem), end='  ')
print('\n')

for i in range(x_gap_len):
    print('{:6.1f}'.format(y_values[i]), end='  ')
    for j in range(x_gap_len):
        print('{:7.2f}'.format(f(x_values[j], y_values[i])), end='  ')
    print('\n')

print('\n-----------------------------------------')
n = int(input('Введите степень полинома: '))  # степень полинома
x = float(input('Введите значение х: '))
y = float(input('Введите значение y: '))

x_conf = initial_config(x, n, x_values)
y_conf = initial_config(y, n, y_values)

# Выборка квадрата начальной кофигурации из матрицы
z_matrix = []
z_string = []
for i in range(n+1):
    for j in range(n+1):
        z_string.append(f(x_conf[j], y_conf[i]))
    z_matrix.append(z_string)
    z_string = []

print('\n---------------------------------------')
print('Начальная конфигурация:')
for i in range(n+1):
    for j in range(n+1):
        print('{:6.2f}'.format(z_matrix[i][j]), end=' ')
    print()


# Интерполяция по x
x_interpolation = []

for i in range(n+1):
    x_interpolation.append(polynomial(n, x, x_conf, z_matrix[i]))

result = polynomial(n, y, y_conf, x_interpolation)

print('\nМой результат:', result)
print('Результат функции:', f(x, y))

