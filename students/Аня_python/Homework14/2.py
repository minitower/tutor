import csv

file = open('./data/2.csv', 'r', encoding='utf-8')

reader = csv.DictReader(file, 
                        delimiter=';', 
                        lineterminator='\n')

arr = []

for row in reader:
    arr.append(row)

file.close()

dict_result = {}

dict_max_value = {}

for i in arr:
    if i['цех'] not in dict_result.keys():
        dict_result[i['цех']] = i['дата']
    if i['цех'] not in dict_max_value.keys():
        dict_max_value[i['цех']] = int(i['количество_единиц'])
    else:
        if int(i['количество_единиц']) > dict_max_value[i['цех']]:
            dict_max_value[i['цех']] = int(i['количество_единиц'])
            dict_result[i['цех']] = i['дата']
        elif int(i['количество_единиц']) == dict_max_value[i['цех']]:
            if i['дата'] < dict_result[i['цех']]:
                dict_result[i['цех']] = i['дата']
                
file = open('./data/2_result.csv', 'w+', encoding='utf-8')

writer = csv.DictWriter(file, 
                        delimiter=';',
                        lineterminator='\n',
                        fieldnames=['цех', 'дата_максимума', 'максимальный_выпуск'])

writer.writeheader()
writer.writerows([{'цех': key, 'дата_максимума': dict_result[key], 'максимальный_выпуск': dict_max_value[key]} for key in dict_result.keys()])

file.close()