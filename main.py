import random
import numpy as np
import multiprocessing as mp
import time

def element_multiply(index, A, B):
    i, j = index
    res = sum(A[i][k] * B[k][j] for k in range(len(B)))
    return (i, j), res

def parallel_matrix_multiply(A, B, result_queue, stop_event):
    if len(A[0]) != len(B):
        raise ValueError("Количество столбцов матрицы A должно быть равно количеству строк матрицы B")

    indices = [(i, j) for i in range(len(A)) for j in range(len(B[0]))]

    try:
        with mp.Pool() as pool:
            results = [pool.apply_async(element_multiply, args=(index, A, B)) for index in indices]
            for result in results:
                if stop_event.is_set():
                    break
                result_queue.put(result.get())
    except Exception as e:
        print(f"Ошибка при умножении матриц: {e}")

def generate_random_matrix(size):
    return np.random.randint(0, 10, size=(size, size))

if __name__ == '__main__':
    matrix_size = int(input("Введите размер квадратных матриц(одно число): "))
    stop_event = mp.Event()
    result_queue = mp.Queue()

    A = generate_random_matrix(matrix_size)
    B = generate_random_matrix(matrix_size)

    try:
        parallel_matrix_multiply(A, B, result_queue, stop_event)

        time.sleep(2)
        stop_event.set()

        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        print("Матрица A:")
        print(A)
        print("\nМатрица B:")
        print(B)
        print("\nРезультат:")
        result_matrix = np.zeros((matrix_size, matrix_size))
        for index, result in results:
            i, j = index
            result_matrix[i][j] = result
        print(result_matrix)
    except ValueError as e:
        print(e)
