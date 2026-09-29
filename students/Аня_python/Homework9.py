import random

n=15

def tup_create(n:int,     
               a = ['A', 'B', 'C', 'D'],
                b = ['open', 'closed', 'in progress'],
                c = [1, 2, 3, 4, 5]):
    '''
    Function for init tuple for task
    
    Args:
        n (int): number of tuple in final tuple
        
    Return:
        tuple of tuple like (a, b, c)
    '''

    result_arr = []
    
    for _ in range(n):
        idx_a = random.randint(0, len(a)-1)
        idx_b = random.randint(0, len(b)-1)
        idx_c = random.randint(0, len(c)-1)
        result_arr.append((a[idx_a], b[idx_b], c[idx_c]))
        
    return tuple(result_arr)
    

tup_1 = tup_create(n)
    
arr_a = []

for i in range(len(tup_1)):
    if tup_1[i][1]=='open' and tup_1[i][2]<=3:
        arr_a.append(tup_1[i][0])
        
        
result = tuple(arr_a)

print(result)