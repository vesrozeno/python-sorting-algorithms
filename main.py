import time
import random

# Função para gerar uma grande quantidade de dados aleatórios
def generate_data(size):
    return [random.randint(0, size) for _ in range(size)]

# Implementações de diferentes algoritmos de ordenação

def bubble_sort(arr):
    print(f"Running bubble_sort on data of size {len(arr)}")
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    print(f"Running insertion_sort on data of size {len(arr)}")
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    print(f"Running selection_sort on data of size {len(arr)}")
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    print(f"Running quick_sort on data of size {len(arr)}")
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    print(f"Running merge_sort on data of size {len(arr)}")
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Função para medir o tempo de execução de cada algoritmo
def measure_time(sort_function, data):
    try:
        start_time = time.time()
        print(f"Measuring time for {sort_function.__name__}")
        sort_function(data.copy())
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"An error occurred in {sort_function.__name__}: {e}")
        raise

# Main
if __name__ == "__main__":
    data_size = 9999  # Tamanho dos dados
    data = generate_data(data_size)

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
    }

    results = []

    for name, func in algorithms.items():
        try:
            duration = measure_time(func, data)
            results.append((name, duration))
            print(f"{name}: {duration:.6f} seconds")
        except Exception as e:
            print(f"Error when running {name}: {e}")
