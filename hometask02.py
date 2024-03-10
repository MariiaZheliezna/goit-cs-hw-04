from time import time
from multiprocessing import Semaphore, Process, Queue
from pathlib import Path

from hometask01 import create_list, read_file

def search_keys(condition, file, keywords, queue):
    with condition:
        text = read_file(file)
        for keyword in keywords:
            if keyword in text:
                queue.put((keyword, str(file)))
                

# Задаємо цільову директорію та ключові слова
folder = Path("./test_files")
keywords = ["успіх", "захист", "глобального", "мета", "новаторства", "легенда"]

# Словник для зберігання результату пошуку
find_result_dic = {}

# Готуємо структуру словника
for keyword in keywords:
    find_result_dic[keyword] = []

def main():
    timer = time()  # Стартуємо відлік часу на виконання
    file_list = create_list(folder)
    condition = Semaphore(3)
    processes = []
    queue = Queue()
    for file in file_list:
        proc = Process(name=str(file), target=search_keys, args=(condition, file, keywords, queue))
        proc.start()
        processes.append(proc)

    # Очікування завершення процессів
    [el.join() for el in processes]

    # Наповнення словнику відповіді з черги
    while not queue.empty():
        rec = queue.get()
        find_result_dic[rec[0]].append(rec[1])

    # Результат в заданому форматі у словнику find_result_dic
    print(find_result_dic)

    # Виводимо час виконання
    print(f"Час виконання: {time() - timer}")

if __name__ == "__main__":
    main()