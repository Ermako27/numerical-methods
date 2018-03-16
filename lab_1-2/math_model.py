from math import sin, exp


def two_args(x, y):
    return (x**3) + (y**2)




def one_arg(x):
    pi = 3.14
    #return x**2-5
    return (x - 1) ** 2 - 0.5*exp(x)
    #return sin((pi/6) * x)
    # return round(sin(x), 4)


""" разделенная разность """
def divided_difference(args, f):
    if len(args) == 1:
        return f(args[0])
    i = args[:-1]
    j = args[1:]
    #print(args[0], args[1])
    #print(i, j)
    #print('--------------')
    #print(divided_difference(j,f))
    return round((divided_difference(i, f) - divided_difference(j, f))/(args[0] - args[-1]), 3)


""" Рассчет полинома Ньютона
    n - степень полинома, x - аргумент полинома"""
def polynomial(n, x, args, f):
    print()
    p = 0
    x_multiply = 1
    y0 = f(args[0])
    if n == 0:
        return y0
    for i in range(n):
        x_multiply *= (x - args[i])
        p += x_multiply * divided_difference(args[:i+2], f)
        print('y', args[:i+2], '=', divided_difference(args[:i+2], f))
    return p + y0


def reverse_divided_difference(args, f):
    if len(args) == 1:
        return f(args[0])
    i = args[:-1]
    j = args[1:]
    #print(args[0], args[1])
    #print(i, j)
    #print('--------------')
    return (args[0] - args[-1])/(reverse_divided_difference(i, f) - reverse_divided_difference(j, f))


def reversed_polynomial(n, y, args, f):
    print()
    p = 0
    y_multiply = 1
    x0 = args[0]
    if n == 0:
        return x0
    for i in range(n):
        y_multiply *= (y - f(args[i]))
        p += y_multiply * reverse_divided_difference(args[:i+2], f)
        print('y', args[:i+2], '=', reverse_divided_difference(args[:i+2], f))
    return round(p + x0, 4)



def main():
    #print(f(6))
    #print(divided_difference((1, 2, 3)))

    print(polynomial(3, 2.3, (1, 2, 3, 4)))
    print(polynomial(3, 2.3, (2, 3, 4, 5)))



if __name__ == '__main__':
    main()




"""
    #x_values = [0.2,0.25,0.27,0.3]
    x_values = [i/2 for i in range(x_gap_len)]  # промежуток иксов на котором идет поиск
    y_values = [one_arg(i) for i in x_values]
   
    for i in range(4):
        print('{:9f} | {:9.3f}'.format(x_values[i], y_values[i]))


    result = reversed_polynomial(n, 0, x_values, one_arg)
    print('-----------------------------------------')
    print('\nРезультат интерполяции: ', result)
    # print('Точное значение: ', f(x))

"""
