from math_model import *

print('1 - Найти значение функции с помощью полинома Ньютона')
print('2 - Найти корни уравнения на отерзке [0-19] методом обратной интерполяции')
print('3 - Найти значение функции нескольких переменных')
choice = int(input('>>> '))


x_gap_len = 22

if choice == 1:

    print('x принадлежит [0.2 - 6.5]')
    print('шаг = 0.3')
    print()
    left = right = 0

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


    n = int(input('Введите степень полинома: '))  # степень полинома
    x = float(input('Введите значение х: '))  # значение в искомой точке




    for i in range(x_gap_len-1):
        if x_values[i] <= x <= x_values[i+1]:

            if (i > 18) and (i < 22):
                right = 22
                left = right - (n + 1)
            elif i == 0:
                left = i
                right = left + n + 1
            else:
                left = i - 1
                right = left + n + 1



    initial_config = tuple(x_values[left:right])  # начальная конфигурация - конкретные узлы на которых идет поиск ( = степень полинома + 1)


    print('\n-----------------------------------------')
    print('Начальная конфигурация:', initial_config)
    print('\n------Значения разделенной разности------', end='')

    result = polynomial(n, x, initial_config, one_arg)
    print('-----------------------------------------')
    print('\nРезультат интерполяции: ', result)
    print('Точное значение: ', one_arg(x))


if choice == 2:


    print('x принадлежит [0.2 - 6.5]')
    print('шаг = 0.3')
    print()

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

    n = int(input('Введите степень полинома: '))  # степень полинома
    # x = float(input('Введите значение х: '))  # значение в искомой точкe


    for i in range(x_gap_len-1):
        if y_values[i] * y_values[i+1] < 0:

            if (i > 18) and (i < 22):
                right = 22
                left = right - (n + 1)
            elif i == 0:
                left = i
                right = left + n + 1
            else:
                left = i - 1
                right = left + n + 1
                print(left, right)

            initial_config = x_values[left:right]

            print('\n-----------------------------------------')
            print('Начальная конфигурация:', initial_config)
            print('\n------Значения разделенной разности------', end='')

            result = reversed_polynomial(n, 0, initial_config, one_arg)
            print('-----------------------------------------')
            print('\nРезультат интерполяции: ', result)
            print('Точный корень: 0.2109', )


if choice == 3:
    n = int(input('Введите степень полинома: '))
    x_values = [i/2 for i in range(x_gap_len)]  # промежуток иксов на котором идет поиск
    y_values = [i/2 for i in range(x_gap_len)]  # промежуток иксов на котором идет поиск
    #z_values = [two_args(x_values[i], y_values[i]) for i in range(x_gap_len)]
    row = []
    z_values = []

    for y in y_values:
        for x in x_values:
            row.append(two_args(x, y))

        z_values.append(row)
        row = []

    print(' Y/X ', end=' | ')

    for i in range(x_gap_len):
        print('{:6.3f}'.format(x_values[i]), end=' | ')
    for i in range(x_gap_len):
        print('{:6.3f}'.format(y_values[i]), end=' | ')
        for j in range(x_gap_len):
            print('{:6.3f}'.format(z_values[j]), end=' | ')

    #for elem in z_values:
     #   print(elem)
