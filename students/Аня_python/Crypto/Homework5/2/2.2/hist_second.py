import matplotlib.pyplot as plt
import math

with open('second_iter.txt', 'r', encoding='utf-8') as f:
    data = f.read().splitlines()
    
data_preprocessed = [i.strip().replace('.', '') for i in data]

hist_arr = []

for i in data_preprocessed:
    hist_arr.extend(i.split())

hist_arr = [int(i) for i in hist_arr]

delta_arr = []

for i in range(len(hist_arr)-1):
    delta_arr.append(hist_arr[i+1] - hist_arr[i])

mean_delta = sum(delta_arr) / len(delta_arr)

interval = [1000, 1300]
mean_interval = (interval[0]+interval[1])/2
ln_delta = math.log(mean_interval, math.e)

plt.hist(delta_arr, bins=20)
plt.title(f'Гистограмма разностей между разницей простых чисел от 1000 до 1300,\n среднее = {mean_delta:.2f}, ln(среднего) = {ln_delta:.2f}', fontsize=10)
plt.xlabel('Разность')
plt.ylabel('Частота')
plt.savefig('delta_hist_20_3.png')