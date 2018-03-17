from math import sin, exp


def one_arg(x):
    pi = 3.14
    #return x**2-5
    return (x - 1) ** 2 - 0.5*exp(x)
    #return sin((pi/6) * x)
    # return round(sin(x), 4)


# разделенная разность
def divided_difference(x_args, y_args):  # x_arags, y_args - tuples
    if len(x_args) == 1:
        return y_args[0]
    y_i = y_args[:-1]
    y_j = y_args[1:]

    x_i = x_args[:-1]
    x_j = x_args[1:]

    x_current_i = x_args[-1]
    x_current_j = x_args[0]

    return round((divided_difference(x_i, y_i) - divided_difference(x_j, y_j)) / (x_current_j - x_current_i), 3)


def polynomial(n, x, x_args, y_args):
    print()
    p = 0
    x_multiply = 1
    y0 = y_args[0]
    if n == 0:
        return y0
    for i in range(n):
        x_multiply *= (x - x_args[i])
        p += x_multiply * divided_difference(x_args[:i+2], y_args[:i+2])
        print('y', y_args[:i+2], '=', divided_difference(x_args[:i+2], y_args[:i+2]))
    return p + y0


# нахождение диапазона иксов содержащего в себе x
def initial_config(x, count, x_args, y_args):  # count - размер диапазона
    close_elem_pos = 0
    delta = abs(x_args[0] - x)
    length = len(x_args)

    for i in range(length):  # нахождение позиции самого близкого по значению элемента
        if abs(x_args[i] - x) < delta:
            close_elem_pos = i
            delta = abs(x_args[i] - x)

    if close_elem_pos < count:
        return x_args[0:count], y_args[0:count]
    elif close_elem_pos > (length - count):
        return x_args[(length - count):], y_args[(length - count):]
    else:
        if count == 0:
            return x_args[close_elem_pos], y_args[close_elem_pos]
        if count == 1:  # если степень полинома == 1
            if x > x_args[close_elem_pos]:
                return x_args[close_elem_pos:close_elem_pos+2], y_args[close_elem_pos:close_elem_pos+2]
            else:
                return x_args[close_elem_pos-1:close_elem_pos+1], y_args[close_elem_pos-1:close_elem_pos+1]
        elif count % 2 == 0:
            i = close_elem_pos-int(count/2)
            j = close_elem_pos+int(count/2)
            return x_args[i:j], y_args[i:j]
        elif count % 2 != 0:
            i = close_elem_pos-int((count-1)/2)
            j = close_elem_pos+int((count-1)/2)
            return x_args[i:j+1], y_args[i:j+1]

    # print(close_elem_pos)




def main():
    pass
    #print(f(6))
    # print(divided_difference((1, 2, 3), (0.5, 0.866, 1)))
    # print(polynomial(2, 1.5, (1, 2, 3), (0.5, 0.866, 1)))

    #print(initial_config(17,5,(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)))


if __name__ == '__main__':
    main()
