from pathlib import Path
from threading import Thread, Semaphore
from time import time


# Задаємо цільову директорію та ключові слова
folder = Path("./test_files")
keywords = ["успіх", "захист", "глобального", "мета", "новаторства", "легенда"]

# Словник для зберігання результату пошуку
find_result_dic = {}

# Готуємо структуру словника
for keyword in keywords:
    find_result_dic[keyword] = []

# Створення списку файлів в цільовій директорії
def create_list(folder:Path):
    file_list = []
    try:
        for obj in folder.iterdir():
            if obj.is_dir():
                res = create_list(obj)
                for f in res:
                    file_list.append(f)
            else:
                file_list.append(obj)
    finally:
        return file_list

# Відкриття файлу на читання
def read_file(file:Path):
    try:
        with open(file, "r", encoding="UTF-8") as f:
            text = f.read()
    except: # якщо файл не текстовий, чи якась похибка відкриття - повертаємо пустий текст
        text = ""
    finally:
        return text

# Пошук у файлі ключів (якщо ключ знайдено, заносимо інформацію в словник find_result_dic)
def search_keys(condition, file, keywords):
    with condition:
        text = read_file(file)
        for keyword in keywords:
            if keyword in text:
                find_result_dic[keyword].append(str(file))

def main():
    timer = time()  # Стартуємо відлік часу на виконання
    file_list = create_list(folder)
    threads = []
    condition = Semaphore(3)
    for file in file_list:
        thread = Thread(name=str(file), target=search_keys, args=(condition, file, keywords))
        thread.start()
        threads.append(thread)
    
    # Очікування завершення потоків
    [el.join() for el in threads]

    # Результат в заданому форматі у словнику find_result_dic
    print(find_result_dic)

    # Виводимо час виконання
    print(f"Час виконання: {time() - timer}")

if __name__ == "__main__":
    main()