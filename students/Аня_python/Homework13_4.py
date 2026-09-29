import math

a, b = -4, 4

h = 1e-5

def f(x):
    return (math.sqrt(x**2+2)*(x**4 - 7 * x**3  + 6*x))/40

def fFirst(x0, x1):
    return (f(x1)-f(x0))/(2*h)

def fSecond(x0, x1, x2):
    return (f(x2)-2*f(x1)+f(x0))/(h**2)

N = math.floor((b - a) / h) + 1

X = [a+i*h for i in range(N)]

FSecond = [fSecond(X[i-1], X[i], X[i+1]) for i in range(1, len(X)-1)]
FSecond = [( f(X[2]) - 2 * f(X[1]) + f(X[0]) )/(h**2)] + FSecond + [
        (f(X[-1]) - 2 * f(X[-2]) + f(X[-3]))/(h**2)
    ]

R = [(X[i] + X[i+1])/2 for i in range(len(FSecond)-1) if FSecond[i]*FSecond[i+1]<0]