import numpy as np
import pandas as pd


def y(x):
    return np.cos(x)


def get_data(a, b, N):
    ox = np.linspace(a, b, N)
    oy = y(ox)
    return ox, oy


def get_x0(a, b):
    x0 = float(input("Input x0: "))
    return x0


def get_node_structure(N, x, y):
    argnum = 5 # a, b, c, d, x
    matrix = np.zeros((N, argnum))

    for i in range(matrix.shape[0]):
        matrix[i][argnum - 1] = x[i] # coefficient b
        matrix[i][0] = y[i] # coefficient a

    return matrix


def print_table(x, y, a, b):
    print("\ny(x) = cos(x); x_i ∈ [%1.2f, %1.2f]; N=10;\n" % (a, b))
    print(pd.DataFrame({"x" : x, "y=y(x)" : y}))


def compute_SLAE(node_structure, N, x, y):

    # node_structure coefficient indeces
    a_ind = 0
    b_ind = 1
    c_ind = 2
    d_ind = 3
    
    # SLAE computing over c[i] coefficient
    alpha = np.zeros((N - 1))
    beta = np.zeros((N - 1))

    for i in range(1, N - 1):
        hi = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z

    # Searching for solution, reverse method
    ind = N - 2
    while (ind > 0):
        node_structure[ind][c_ind] = alpha[ind] * node_structure[ind + 1][c_ind] + beta[ind]
        ind -= 1

    # Now we have c[i-th] coefficients and we can find b[i-th] and d[i-th] coefficients
    ind = N - 1
    while (ind > 0):
        hi = x[ind] - x[ind - 1]
        node_structure[ind][d_ind] = (node_structure[ind][c_ind] - node_structure[ind - 1][c_ind]) / hi
        node_structure[ind][b_ind] = hi * (2.0 * node_structure[ind][c_ind] + node_structure[ind - 1][c_ind]) / 6.0 + (y[ind] - y[ind - 1]) / hi
        ind -= 1

    return alpha, beta, node_structure


def interpolate(node_structure, x0, N):
    n = node_structure.shape[0] # node_structure length

    if (x0 <= node_structure[0][-1]): # if x0 lower than net point x[0], use first element
        s = node_structure[0]
    else:
        if (x0 >= node_structure[N - 1][-1]): # if x0 greater than net point  x[N - 1], use the last element
            s = node_structure[N - 1]
        else: # x lays in interval [a, b], using binary search
            i = 0
            j = N - 1
            while (i + 1 < j):
                k = int(i + (j - i) / 2)
                if (x0 <= node_structure[k][-1]):
                    j = k
                else:
                    i = k
            s = node_structure[j]

    dx = x0 - s[-1]

    return s[0] + (s[1] + (s[2] / 2.0 + s[3] * dx / 6.0) * dx) * dx


def print_node_structure(node_structure):
    print(pd.DataFrame(node_structure, columns=["a", "b", "c", "d", "x"]))


def main():
    pi = np.pi
    a = -pi
    b =  pi
    N = 7

    # Get data
    x, y = get_data(a, b, N)
    print_table(x, y, a, b)

    # Asking for x0
    x0 = get_x0(a, b)

    # Get structure matrix
    node_structure = get_node_structure(N, x, y)
    alpha, beta, node_structure = compute_SLAE(node_structure, N, x, y)
    print_node_structure(node_structure)
    print("\nAnswer: %4.8f" % (interpolate(node_structure, x0, N)))


if __name__ == "__main__":
    main()
