a = {12, 21, 13, 31, 41, 51, 61, 14}

tmp_arr = []
result = []

for i in range(len(a)):
    x = a.pop()
    tmp_arr.append(set([str(x)[i] for i in range(len(str(x)))]))

for i in range(len(tmp_arr)):
    for ii in range(len(tmp_arr)):
        if i != ii and tmp_arr[i]==tmp_arr[ii] and tmp_arr[i] not in result:
            result.append(tmp_arr[i])
            
print(result)