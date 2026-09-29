from scipy.optimize import fmin, bisect
import math

a, b = -4, 4

def f(x):
    return (math.sqrt(x**2+2)*(x**4 - 7 * x**3  + 6*x))/40

root_arr = []

bisect_tol = 1e-7

root_1 = round(bisect(f, -4, -0.528, xtol=bisect_tol), 7)
root_2 = round(bisect(f, 0.6, 4, xtol=bisect_tol), 7)
root_3 = round(bisect(f, -0.528, 0.6, xtol=bisect_tol), 7)

min_arr = []
max_arr  = []

for i in [root_1, root_2, root_3]:
    min = fmin(f, i, xtol=bisect_tol)[0]
    max = fmin(lambda x: -f(x), i, xtol=bisect_tol)[0]
    
    if min>=a and min<=b:
        min_arr.append(min.round(7))
    if max>=a and max<=b:
        max_arr.append(max.round(7))

min_values = list(set(min_arr))
max_values = list(set(max_arr))

print(min_values)
print(max_values)