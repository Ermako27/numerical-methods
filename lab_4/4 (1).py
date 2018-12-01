import numpy as np
import pandas as pd
import glob

from matplotlib import pyplot as plt

WEIGHTS_NOT_FOUND = 0

def f(x):
    return x*np.sin(x)


def get_table(a, b, ndots):
    table = np.zeros((3, ndots)) # 3 is x, y, w

    # Weigts loading
    w = [1,2,3,4,5,6,7,8,9,10]
    if (w == WEIGHTS_NOT_FOUND):
        weights = np.ones((ndots))
    else:
        weights = np.ones((ndots))
        for d in range(len(w)):
            weights[int(w[d][0])] = float(w[d][1]) # Fill weights

    x = np.linspace(a, b, ndots)
    y = f(x)

    # Fill the table by x vector
    for i in range(x.shape[0]):
        table[0][i] = x[i]

    # Fill the table by y vector
    for i in range(y.shape[0]):
        table[1][i] = y[i]

    # Fill the table by weights
    for i in range(weights.shape[0]):
        table[2][i] = weights[i]

    return table


def phi(x, k, y=False, with_y=False):
    # a - numpy vector of coefficients
    # x - numpy vector
    # k - degree
    # Ф(x, a) = sum(a_k * ф_k(x))_i for i=(0, ..., n)
    if (with_y == False):
        return np.sum(x ** k)
    else:
        return np.sum((x ** k) * y)


def load_weights():
    fname = "./weights.txt"
    if (fname in glob.glob("./*.txt")):
        file = open(fname, "r")
        w = [tuple(i[:-1].split(' ')) for i in open("./weights.txt", "r").readlines()]
        if (len(w) == 0):
            print("Weights not found! Default w_i=1 for each y_i")
            return 0
        else:
            return w
    else:
        print("Weights file doesn't exists! Default w_i=1 for each y_i")
        return 0
    

def get_slae(x, y, k, w):
    # Create matrix A and b
    A = np.zeros((k + 1, k + 1))
    b = np.zeros((k + 1, 1))

    # A formation
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i][j] = w[i] * phi(x, i + j)

    # b formation
    for i in range(b.shape[0]):
        b[i] = w[i] * phi(x, i, y=y, with_y=True)

    return A, b


def solve_slae(A, b):
    # Returns a0, ..., ak coeficients
    return np.linalg.solve(A, b)


def plot_approximated(x, y, x_fitted, y_fitted, legend=['y=f(x)', 'Approximated Ф(x)~f(x)']):
    plt.title('Function approximation')
    plt.grid(True)
    plt.plot(x, y, x_fitted, y_fitted, "r")
    plt.plot(x, y, "or")
    plt.legend(legend)
    plt.show()


def print_table(table):
    print(pd.DataFrame(table.T, columns=['x', 'y=sin(x)', 'w']))


def set_params():
    a = float(input("Input a: ") or -10)
    b = float(input("Input b: ") or 10)
    ndots = int(input("Input ndots: ") or 10)
    degree = int(input("Input Pn(x) degree: ") or 5)

    return a, b, ndots, degree


# def test():
#     x = np.array([i for i in range(1, 9)])
#     y = np.array([5.95, 20.95, 51.9, 105, 186, 301, 456.1, 657.1])

#     A, b = get_slae(x, y, 3, np.ones(x.shape))
#     c = solve_slae(A, b)
#     print(c)
    


def compute_polynom(x, coefs):
    fitted_value = 0
    for i in range(len(coefs)):
        fitted_value += coefs[i] * (x ** i)

    return fitted_value


def get_fitted_space(x, coefs, ndots):
    # x = np.array()
    y = np.array([compute_polynom(i, coefs) for i in x])

    return x, y


# Set main configs
a, b, ndots, degree = set_params()
table = get_table(a, b, ndots)
print_table(table)

# System solving
x = table[0]
y = table[1]
w = table[2] # weights
A, B = get_slae(x, y, degree, w)
coefficients = solve_slae(A, B)
print("\n", pd.DataFrame(coefficients, columns=['Polynom coefficients']))
x_fitted, y_fitted = get_fitted_space(x, coefficients, ndots)

# Plotting results
plot_approximated(x, y, x_fitted, y_fitted)


"""
if __name__ == "__main__":
    main()
"""
