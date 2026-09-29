import matplotlib.pyplot as plt
import math
import glob

files = glob.glob('*.txt')

print(files)

dict_res = {}

for i in files:
    with open(i, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
        
        data_preprocessed = [i.strip().replace('.', '') for i in data]

        hist_arr = []

        for ii in data_preprocessed:
            hist_arr.extend(ii.split())
        
        dict_res.update({int(i.split('.')[0].replace('k', '')): len(hist_arr)})

plt.bar(dict_res.keys(), dict_res.values())
plt.title('Количество найденных простых чисел от k')
plt.xlabel('k')
plt.ylabel('Количество простых чисел')
plt.savefig('hist.png')