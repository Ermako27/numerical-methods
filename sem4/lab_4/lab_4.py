import numpy as np
import pandas as pd
# import glob

from matplotlib import pyplot as plt


def phi(x, k, y=False, with_y=False):
    # a - numpy vector of coefficients
    # x - numpy vector
    # k - degree
    # Ф(x, a) = sum(a_k * ф_k(x))_i for i=(0, ..., n)
    if (with_y == False):
        return np.sum(x ** k)
    else:
        return np.sum((x ** k) * y)


def read_file(path):
    data_points = pd.read_csv(path, delimiter=";", names=['X', 'Y', 'W'])
    # print(data_points.X)
    X = list(data_points.X)
    Y = list(data_points.Y)
    W = list(data_points.W)
    return np.array(X), np.array(Y), np.array(W), data_points


def get_slae(x, y, k, w):
    # Create matrix A and b
    A = np.zeros((k + 1, k + 1))
    b = np.zeros((k + 1, 1))
    # print(w)

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


def plot_approximated(x, y, x_fitted, y_fitted, legend=['Approximated Ф(x)~f(x)', 'y=f(x)']):
    plt.title('Function approximation')
    plt.grid(True)
    plt.plot(x_fitted, y_fitted, "r")
    plt.plot(x, y, "ob")
    plt.legend(legend)
    plt.show()


def print_table(table):
    # print(pd.DataFrame(table.T, columns=['x', 'y', 'w']))
    pass


def set_params():
    ndots = int(input("Amount of points: ") or 10)
    degree = int(input("Degree: ") or 5)

    return ndots, degree


def test():
    x = np.array([i for i in range(1, 9)])
    y = np.array([5.95, 20.95, 51.9, 105, 186, 301, 456.1, 657.1])

    A, b = get_slae(x, y, 3, np.ones(x.shape))
    c = solve_slae(A, b)
    print(c)
    


def compute_polynom(x, coefs):
    fitted_value = 0
    for i in range(len(coefs)):
        fitted_value += coefs[i] * (x ** i)

    return fitted_value


def get_fitted_space(start, end, coefs, ndots):
    x = np.arange(start, end + (end-start)/ndots, (end-start)/ndots)
    y = np.array([compute_polynom(i, coefs) for i in x])

    return x, y


# Set main configs
x, y, w, out_table = read_file("data.csv")
print(out_table)
ndots, degree = set_params()


# # System solving
# x = table[0]
# y = table[1]
# w = table[2] # weights

A, B = get_slae(x, y, degree, w)
coefficients = solve_slae(A, B)
print("\n", pd.DataFrame(coefficients, columns=['Polynom coefficients']))
x_fitted, y_fitted = get_fitted_space(x[0], x[-1], coefficients, ndots)

# Plotting results
plot_approximated(x, y, x_fitted, y_fitted)


"""
if __name__ == "__main__":
    main()
"""
