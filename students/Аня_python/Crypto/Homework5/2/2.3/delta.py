import math

numbers = [29, 47, 71, 113, 149]
k = [10, 15, 20, 30, 35]

aprox = [i/math.log(i, math.e) for i in k]

for i in numbers:
    print('Относительная погрешность:', (abs(i - aprox[numbers.index(i)])/i)*100, '%')
