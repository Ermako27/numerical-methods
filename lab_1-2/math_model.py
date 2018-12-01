from math import cos, sin, exp


def one_arg(x):
    pi = 3.14
    #return x**2-5
    # (x - 1) ** 2 - 0.5*exp(x)
    #return sin((pi/6) * x)
    # return round(sin(x), 4)
    return cos(x)


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
def initial_config(x, count, x_args, y_args):  # count - размер диапазона (степень полинома)
    copy_count = count + 1 # чтобы взять корней на 1 больше
    close_elem_pos = 0  # позиция самого близкого по значению элемента (можно считать эту позицию позицией корня)
    delta = abs(x_args[0] - x)
    length = len(x_args)

    for i in range(length):  # нахождение позиции самого близкого по значению элемента
        if abs(x_args[i] - x) < delta:
            close_elem_pos = i
            delta = abs(x_args[i] - x)
    # print('QWER', x_args[close_elem_pos])

    if close_elem_pos < copy_count:  # если позиция корне меньше количества корней
        return x_args[0:copy_count], y_args[0:copy_count]  # то взять все значения до позиции, численной равной количеству необходимых корней

    elif close_elem_pos > (length - copy_count):
        return x_args[(length - copy_count):], y_args[(length - copy_count):]
    else:
        if count == 0:  # степень полинома = 0 -> вернуть один корень
            return x_args[close_elem_pos], y_args[close_elem_pos]
        if count == 1:  # если степень полинома == 1
            if x > x_args[close_elem_pos]:
                # print("conf", x_args[close_elem_pos:close_elem_pos+2])
                return x_args[close_elem_pos:close_elem_pos+2], y_args[close_elem_pos:close_elem_pos+2]
            else:
                return x_args[close_elem_pos-1:close_elem_pos+1], y_args[close_elem_pos-1:close_elem_pos+1]
        elif count % 2 == 0:
            i = close_elem_pos-int(copy_count/2)
            j = close_elem_pos+int(copy_count/2)
            return x_args[i:j], y_args[i:j]
        elif count % 2 != 0:
            i = close_elem_pos-int((copy_count-1)/2)
            j = close_elem_pos+int((copy_count-1)/2)
            return x_args[i:j+1], y_args[i:j+1]

    # print(close_elem_pos)




def main():
    #print(f(6))
    # print(divided_difference((1, 2, 3), (0.5, 0.866, 1)))
    # print(polynomial(2, 1.5, (1, 2, 3), (0.5, 0.866, 1)))

    print(initial_config(17,5,(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)))


if __name__ == '__main__':
    main()
