"""
Есть N файлов excel в папке. В файлах лежит информация о планах работы и сотрудниках участвующих в проектах.
Файлы внутри выглядят так:

Название проекта	Руководитель	Дата сдачи план.	Дата сдачи факт.	Иванов Р.А.
план.	Иванов Р.А.
факт.	Петров И.И.
план.	Петров И.И.
факт.	Сидоров М.В.
план.	Сидоров М.В.
факт.
Проект1	Иванов Р.А.	1.10.2013	30.09.2013	1	3		1	2	2
Проект2	Сидоров М.В.	15.10.2013	16.10.2013	1	1	10	9	0

Колонки:
•	Название проекта
•	Руководитель – сотрудник ответственный за проект
•	Дата сдачи (палн и факт) – планируемая и фактическая дата сдачи проекта
•	Список сотрудников (план и факт) – сколько человеко-дней каждого сотрудника потрачено на проект по плану и по факту.

Сотрудников и проектов может быть сколько угодно в каждом файле.
В каждом файле полезная информация лежит только на первом листе.
Необходимо по этим файлам оценить успешность сотрудников. Критерий для успешности выбрать самому.
Сделать вывод списка сотрудников в порядке их успешности по выбранному критерию.
Цели
1. Продемонстрировать работоспособность механизма.
2. Продумать, как в дальнейшем расширять эту задачу: как реализовать технически, как именно по функционалу можно
расширять задачу.

Требования к выполнению задачи
1.	Задача выполняется на Python.
2.	Желательно с использованием сторонних библиотек.
3.	Решение должно состоять из:
a.	документа описывающего текущее решение и перспективы его расширения;
b.	исходных файлов (которые можно выполнить и посмотреть на работу программы);
c.	сторонних библиотек, которые нужны для работы (или ссылок на них).
"""

import os
import datetime
import pandas as pd

STAT_DIR = "projects_stat"
LOG_FILE = "log.txt"
EMPLOYERS_RAITING = dict()


def logger(message: str):
    """
    Модуль логирования, выводит текст в консоль и записывает в файл log.txt
    :param message: Сообщение в лог
    :return:
    """
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{datetime.datetime.now()} - {message} \n")


def get_stat_files(stat_tables_dir: str) -> list:
    logger("Начинаем поиск таблиц в папке")
    tables = os.listdir(path=stat_tables_dir)
    logger(f"Найдено {len(tables)} файлов")
    return tables


def stat_file(file_name: str):
    file_path = f'./{STAT_DIR}/{file_name}'
    file = pd.read_excel(file_path)
    result = file.to_dict()
    print(result)
    for i in range(len(result["Название проекта"])):
        for key, value in result.items():
            print(key, value[i])
            add_data_employer("Завершил проектов", result["Руководитель"][i], 1)
            date_plane = result["Дата сдачи план."][i]
            date_fact = result["Дата сдачи факт."][i]
            if (date_plane - date_fact).days >= 0:
                add_data_employer("Завершил проектов в срок", result["Руководитель"][i], 1)
            if key.endswith(" план.") and not key.startswith("Дата "):
                pass
                #add_data_employer("Участвовал в проектах", key[:-6], 1)
                #add_data_employer("Плановых дней в проекте", key[:-6], value[i])


def add_data_employer(field, name, data):
    if name not in employers:
        employers.update({name: {
            "Завершил проектов": 0,
            "Завершил проектов в срок": 0,
            "Участвовал в проектах": 0,
            "Плановых дней в проекте": 0,
            "Уложился в плановые": 0
        }})
    employers[name][field] += data


def unpack_stat_files(files_list: list):
    for file in files_list:
        stat_file(file)


employers = {}

if __name__ == "__main__":
    logger("Начали")
    stat_files = get_stat_files(STAT_DIR)
    unpack_stat_files(stat_files)
    for key, value in employers.items():
        print(key, value)
    logger("Закончили работу \n")
