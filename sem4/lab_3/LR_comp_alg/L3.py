from matplotlib import pyplot as plt
import numpy as np
from math import *


def m0(x, y, h):
  	return (4*y[1] - y[2] - 3*y[0]) / (2*((x[1] - x[0]) / h))

def mN(y, h):
  	N = y.shape[0] - 1
  	return (3*y[N] - y[N-2] - 3*y[N-1]) / (2*h)

    
def m_i(i, x, y, h, N):
    if (i == 0):
        return m0(x, y, h)
    if (i == (N-1)):
        return mN(y, h)

    return((y[i+1] - y[i-1])/(2*h))

def find(x0, x):
    if (x0 > x[0] and x0 < x[-1]):
        for i in range(len(x)):
            if (x0 > x[i]):
                i_a = i
                i_b = i+1
        return i_a, i_b

    if x0 == x[0]:
        return 0, 1
    if x0 == x[-1]:
        return len(x)-2, len(x)-1
      

def y(x):
    return np.cos(x)


def get_data(a, b, N):
    ox = np.linspace(a, b, N)
    oy = y(ox)
    return ox, oy

def get_h(a, b, N):
    return (b-a)/(N-1)


def S3(x0, h, x, y, N):
    i_s, i_f = find(x0, x)

    result = ((x[i_f]-x0)**2) * (2*(x0-x[i_s]) + h) / (h**3) * y[i_s]
    result += ((x0 - x[i_s])**2) * (2*(x[i_f]-x0) + h) / (h**3) * y[i_f]
    result += ((x[i_f]- x0)**2)*(x0-x[i_s]) / (h**2) * m_i(i_s, x, y, h, N)
    result += ((x0 - x[i_s])**2)*(x0 - x[i_f]) / (h**2) * m_i(i_f, x, y, h, N)

    return result
                                    
    
def main():
    a = float(input("Введите нижнюю границу интерполяционной сетки a: "))
    b = float(input("Введите верхнюю границу интерполяционной сетки b: "))
    N = int(input("Введите количество отрезков в сетке N: "))
    x0 = float(input("Введите x для интерполяции: "))
    
    ox, oy = get_data(a, b, N)
    h = get_h(a, b, N)

    plt.grid(True)
    plt.plot(ox, [S3(i, h, ox, oy, N) for i in ox])
         
    
    print(S3(x0, h, ox, oy, N))
    plt.plot(x0, S3(x0, h, ox, oy, N), "og")
    plt.show()
    
if __name__ == '__main__':
    main()

