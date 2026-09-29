from scipy.optimize import bisect
import math

def f(x):
    return (math.sqrt(x**2+2)*(x**4 - 7 * x**3  + 6*x))/40

root_arr = []

bisect_tol = 1e-7

root_1 = round(bisect(f, -4, -0.528, xtol=bisect_tol), 7)
root_2 = round(bisect(f, 0.6, 4, xtol=bisect_tol), 7)
root_3 = round(bisect(f, -0.528, 0.6, xtol=bisect_tol), 7)

print(root_1, root_2, root_3)