arr_init = [
    'W119; сотрудник: Климов И.С.; задания: [{тип: отчет, время: 3.2}, {тип: отчет, время: 3.2}, {тип: презентация, время: 2.1}]',
    'W201; сотрудник: Петров Ф.С.; задания: [{тип: отчет, время: 5.1}, {тип: презентация, время: 3.8}]',
    'W220; сотрудник: Иванов П.Р.; задания: [{тип: отчет, время: 6.2}, {тип: презентация, время: 1.1}]',
    'W222; сотрудник: Расторгуев Т.С.; задания: [{тип: отчет, время: 3.1}, {тип: презентация, время: 10.1}]',
    ]

dict_res = {}


for i in arr_init:
    split_arr = i.split(';')
    tmp_id = split_arr[0]
    tmp_task = split_arr[2][11:-1].split(',')
    tmp_dict_arr = []
    for i in tmp_task:
        if '{' in i:
            tmp_dict = {}
            i = i.replace('{', '')
            tmp_dict.update({i.split(':')[0].strip(): i.split(':')[1].strip()})
        elif '}' in i:
            i = i.replace('}', '')
            tmp_dict.update({i.split(':')[0].strip(): i.split(':')[1].strip()})
            tmp_dict_arr.append(tmp_dict)
        else:
            tmp_dict.update({i.split(':')[0].strip(): i.split(':')[1].strip()})
    dict_res.update({tmp_id: tmp_dict_arr})
    
arr_time = []

for employee in list(dict_res.values()):
    tmp_time = []
    for task in employee:
        if task['тип'] == 'отчет':
            tmp_time.append(float(task['время']))
    arr_time.append(tmp_time)
    
result_arr = []

for idx, report_time in enumerate(arr_time):
    if sum(report_time)>5:
        result_arr.append(list(dict_res.keys())[idx])
        
result_arr