from math_model import *
x_gap_len = 20
x_values = []
ar = 0.20
for i in range(x_gap_len):
    x_values.append(ar)
    ar += 0.3

y_values = [one_arg(i) for i in x_values]

print('\n-----------------------------------------')
print('     X             Y')

for i in range(x_gap_len):
    print('{:9.3f} | {:9.3f}'.format(x_values[i], y_values[i]))

print('\n1 - Найти значение функции с помощью полинома Ньютона')
print('2 - Найти корни уравнения на отерзке [0-19] методом обратной интерполяции')
choice = int(input('>>> '))


if choice == 1:

    n = int(input('Введите степень полинома: '))  # степень полинома
    x = float(input('Введите значение х: '))

    x_config, y_config = initial_config(x, n, x_values, y_values)

    # print('\n-----------------------------------------')
    print('Начальная конфигурация:', x_config)
    print('\n------Значения разделенной разности------', end='')

    result = polynomial(n, x, x_config, y_config)
    print('-----------------------------------------')
    print('\nРезультат интерполяции: ', round(result, 4))
    print('Точное значение: ', round(one_arg(x), 4))


if choice == 2:

    n = int(input('Введите степень полинома: '))  # степень полинома

    y_config, x_config = initial_config(0, n, y_values, x_values)

    # print('\n-----------------------------------------')
    # print('Начальная конфигурация:', config)
    print('\n------Значения разделенной разности------', end='')

    result = polynomial(n, 0, y_config, x_config)
    print('-----------------------------------------')
    print('\nРезультат интерполяции: ', round(result, 4))
    print('Точный корень: 0.2109')
