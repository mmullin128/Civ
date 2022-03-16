import random

def partition(arr,low,high,keys=None):
    pivot = arr[high]
    if keys:
        pivotKeys = []
        for k in range(len(keys)):
            pivotKeys.append(keys[k][high])
    i = low
    j = high-1
    if i == j:
        if arr[i] < pivot:
            i = high
    while i < j:
        while arr[i] < pivot and i < high:
            i += 1
        while arr[j] >= pivot and j > 0:
            j -= 1
        if i < j:
            Ai = arr[i]
            Aj = arr[j]
            arr[i] = Aj
            arr[j] = Ai
            if keys:
                for k in range(len(keys)):
                    Ki = keys[k][i]
                    Kj = keys[k][j]
                    keys[k][i] = Kj
                    keys[k][j] = Ki
    arr[high] = arr[i]
    arr[i] = pivot
    if keys:
        for k in range(len(keys)):
            keys[k][high] = keys[k][i]
            keys[k][i] = pivotKeys[k]
    return i
def quicksort(arr,low,high,keys=None):
    if low < high:
        j = partition(arr,low,high,keys=keys)
        quicksort(arr,low,j-1,keys=keys)
        quicksort(arr,j+1,high,keys=keys)

def test(arr=None):
    if arr:
        print(arr)
        quicksort(arr,0,len(arr)-1)
        print(arr)
        return
    arrays = []
    keysArray = []
    for a in range(100):
        array = []
        keys = [[],[]]
        for b in range(random.randint(0,100)):
            num = random.random()
            array.append(num)
            keys[0].append(str(num))
            keys[1].append(str(num) + '0')
        arrays.append(array)
        keysArray.append(keys)
    for a in range(len(arrays)):
        arr = arrays[a]
        keyArr = keysArray[a]
        quicksort(arr,0,len(arr)-1,keys=keyArr)
        for i in range(len(arr)):
            if i == 0:
                continue
            prevI = i - 1
            diff = arr[i] - arr[prevI]
            if diff < 0:
                print('!!error in quicksort!!')
                return
            if arr[i] != eval(keyArr[0][i]) and str(arr[i]) != keyArr[0][i] + '0':
                print('error with quicksort keys: ')
                return
test()#arr=[8,9,7,4,2,4,4,5,1,5])
