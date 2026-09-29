import fnmatch

with open("./data/file1.txt", "r", encoding='utf-8') as f:
    data = f.read()
    
arr = data.split('\n')
result = []

template = input('Напишите строку-шаблон для поиска: ')

for str in arr:
    if fnmatch.fnmatch(str, template):
        result.append(str)

with open("./data/file2.txt", "w+", encoding='utf-8') as f:
    f.write('\n'.join(result))