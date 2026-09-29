import matplotlib.pyplot as plt
import math
import numpy as np

def f(x):
    return (math.sqrt(x**2+2)*(x**4 - 7 * x**3  + 6*x))/40

def fFirst(x0, x1):
    return (f(x1)-f(x0))/(2*h)

def fSecond(x0, x1, x2):
    return (f(x2)-2*f(x1)+f(x0))/(h**2)

a, b = -4, 4

N = 1000 + 1

h = ( b - a ) / ( N - 1)

X = [a+i*h for i in range(N)]

F = [f(x) for x in X]

FFirst = [fFirst(X[i-1], X[i+1]) for i in range(1, len(X)-1)]
FFirst = [(f(X[1]) - f(X[0]))/h] + FFirst + [(f(X[-1]) - f(X[-2]))/h]

FSecond = [fSecond(X[i-1], X[i], X[i+1]) for i in range(1, len(X)-1)]
FSecond = [( f(X[2]) - 2 * f(X[1]) + f(X[0]) )/(h**2)] + FSecond + [
        (f(X[-1]) - 2 * f(X[-2]) + f(X[-3]))/(h**2)
    ]

plt.figure(figsize=(10, 6))
plt.plot(X, F, label='f(x)')
plt.plot(X, FFirst, label='Первая производная')
plt.plot(X, FSecond, label='Вторая производная')
plt.title('График функции (sqrt(x**2+2)*(x**4 - 7 * x**3  + 6*x))/40 и ее двух производных')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)