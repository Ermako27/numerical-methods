import pandas as pd
import numpy as np


def f(x):
	return np.cos(x) # -np.arctan(x-1.7)


def generate_points(func, x_points, weights=None, file=None):
	"""
	input: 
	func - math func
	x_points - int or list 
		if int --> generates by range(int)
	retuning data structured as tuple(X, Y)
	"""
	if type(x_points) == int:
		X = np.arange(x_points)
	else:
		X = x_points

	if weights == None:
		W = np.random.rand(len(x_points))
	elif weights == 1:
		W = [1 for i in range(len(X))]
	else:
		W = weights


	Y = []
	for i in X:
		Y.append(func(i))

	if file != None:
		for i in zip(X, Y, W):
			file.write(str(i[0]) + ";" + str(i[1]) + ";" + str(i[2]) + "\n")

	return X, Y, W


# p = generate_points(f, np.arange(-10, 10, 0.5))
# print(p, p[0])

file_write = open("data.csv","w")
X, Y, W = generate_points(f, np.arange(0, 10, 1), weights=1, file=file_write )
# print(X, Y, W)
file_write.close()

# x = np.random.rand(100)*4.0-2.0
# y = np.random.rand(100)*4.0-2.0
# z = x*np.exp(-x**2-y**2)
# ti = np.linspace(-2.0, 2.0, 100)
# XI, YI = np.meshgrid(ti, ti)

# print(z)
