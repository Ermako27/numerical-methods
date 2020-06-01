from matplotlib import pyplot as plt
import numpy as np
from math import *


class Approximator(object):

    def read_input(self):
        self.degree = int(input("Введите степень полинома: "))
        self.x0 = float(input("Введите x0: "))

        return self.degree, self.x0
    

    def plot(self, x, y, x_approx, y_approx, x0, y0, MSE, MAE, my_root):


        plt.title("Approximation for -x^3")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)


        plt.plot(x, y, "o-", color="#00cdcd", lw=1)
        plt.plot(x_approx, y_approx, color="#a570ff")
        plt.plot(x0, y0, "og")
        plt.plot(my_root, self.f(my_root), 'bo')
        
        plt.legend(["Func", "Approximation", "Value", "Root"])


    def approximate(self, x, y, x0, degree):


        def dot_product(x0, x):
            product = 1

            for x_i in x:
                product *= (x0 - x_i)

            return product

        def polynof_coef(x, y):
            
            
            if ((len(x) == 1) or (len(x) == 0)):
                return 1

            if (len(x) == 2):
                return (y[0] - y[1]) / (x[0] - x[1])
            else:
                return (polynof_coef(x[:-1], y[:-1]) - polynof_coef(x[1:], y[1:])) / (x[0] - x[-1])

        def calculate_approximation(x, y, x0, n):
            sigma = y[0]
            for k in range(1, n + 1):
                sigma += dot_product(x0, x[:k]) * polynof_coef(x[:k + 1], y[:k + 1])

            return sigma


        fitted_value = calculate_approximation(x, y, x0, degree)

        return fitted_value


    def get_x_segment(self, n_points, a=-10, b=10):

        #
        return np.linspace(a, b, n_points)


    def get_y_segment(self, x):
        return self.f(x)


    def f(self, x):
        return x*x*x


    def compute_MSE_MAE(self, x, N_nearest_list, y_true_global, y_pred):
        
        start_i = np.where(x == N_nearest_list[0])
        start_i = start_i[0][0]

        MSE = 0
        MAE = 0

        for i in range(len(y_pred)):
            MSE +=    (y_true_global[i + start_i] - y_pred[i])**2
            MAE += abs(y_true_global[i + start_i] - y_pred[i])

        return MSE, MAE


    def get_x0_nearest(self, x0, x, N):
            
        if N == 0:
            N = 2

        x_prev = 0
        x_next = 0
        N_nearest = []

        
        for i in range(0, len(x)-1):
            
            if x0 > x[i] and x0 < x[i + 1]:
                x_prev = x[i]
                x_next = x[i + 1]

                tmp_c = 0
                t = 0
                j = -1

                if N %2 != 0:
                    while t != (N // 2 - 1) and j != 0:
                        j = i + tmp_c
                        N_nearest.append(x[j])
                        tmp_c -= 1
                        t += 1
                    N_nearest = [k for k in reversed(N_nearest)]
                else:
                    while t != N // 2 and j != 0:
                        j = i + tmp_c
                        N_nearest.append(x[j])
                        tmp_c -= 1
                        t += 1
                N_nearest = [k for k in reversed(N_nearest)]
                    
               
                
                tmp_c = 0
                t = 0
                j = -1
                while t != N // 2 and j != 0:
                    j = i + tmp_c
                    N_nearest.append(x[j + 1])
                    tmp_c += 1
                    t += 1
                break


        return N_nearest


    def run(self):

        flag = 1
        if flag == 1:
            a = float(input("Введите нижнюю границу интервала a: "))
            b = float(input("Введите верхнюю границу интервала b: "))
            if a > b:
                a, b = b, a
                
        result_root = []

        #вывод точек
        self.segment_n_points = 30
        

        X = self.get_x_segment(n_points=self.segment_n_points)
        y = self.get_y_segment(X)

    

        if flag == 1:
            aa, bb = self.find_root(a, b, X, y)
            
        #параметры
        degree, x0 = self.read_input()

        print("|     x      |      y    |")
        for i in range(len(X)):
            print("|{:4.5f} | {:4.5f}".format( X[i], y[i]))

        self.N_nearest = degree + 1

        #получение точек
        N_nearest_list = np.array(self.get_x0_nearest(x0, X, self.N_nearest))
        y_on_N_nearest = self.get_y_segment(N_nearest_list)

        result = []
        for n in N_nearest_list:
            result.append(self.approximate(N_nearest_list, y_on_N_nearest, n, degree))
            if flag == 1:
                result_root.append(self.approximate(bb, aa, 0, degree))

        if flag == 1:
            my_root =  self.approximate(bb, aa, 0, degree)
            print("Найденный корень:", my_root)

        MSE, MAE = self.compute_MSE_MAE(X, N_nearest_list, y, result)


        self.plot(X,
                  y,
                  N_nearest_list,
                  result,
                  x0,
                  self.approximate(N_nearest_list,
                                   y_on_N_nearest,
                                   x0,
                                   degree),
                  MSE,
                  MAE, my_root)
        
        plt.show()


    def find_root(self, a, b, X, y):
        
        x_s = 0
        x_e = 0
        
        for x_i in X:
            if a > x_i:
                x_s = x_i
            if b >= x_i:
                x_e = x_i

        X = list(X)
        ind_x_s = X.index(x_s)
        ind_x_e = X.index(x_e)

        X_a = []
        Y_a = []

        for i in range(ind_x_s, ind_x_e + 1):
            X_a.append(X[i])
            Y_a.append(self.f(X[i]))

        return X_a, Y_a

        


def main():
    i = Approximator()
    i.run()

if __name__ == '__main__':
    main()
