from typing import List, Tuple, Dict

def download_file(file_path: str) -> Tuple[int, List[str]]:
    """
        Функция для чтения файла по заданному пути. Извлекает из него норму рабочих часов ииз первой
        строки и записи о списаниях

        Params:
                file_path - путь к файлу со списаниями

        Returns:
                Кортеж, состоящий из числа-нормы рабочих часов и списока строк списаний
        """
    with open(file_path, 'r', encoding='utf-8') as file:
        # Чтение первой строки файла и преобразование в int
        norm = int(file.readline().strip())
        # Чтение оставшихся строк в список
        records = file.readlines()

    return norm, records

def find_disbalance(norm: int, records: List[str]) -> Dict[str, int]:
    """
        Функция определяет дизбаланс относительно заданной нормы, основываясь на полученном списке о списаниях

        Params:
                norm - норма рабочих часов на неделю для одного сотрудника
                records - список строк с информацией о списании времени сотрудника

        Returns:
                Словарь, у которого ключи - полные имена сотрудников вида <Фамилия И.О.>,
                значения - дизбаланс списанных часов относительно нормы с соответствующим знаком (положительное
                значение означает переработку, отрицательное - недоработку)

        """
    disbalance = {}
    for record in records:
        # Удаление начальных и конечных пробелов и разделение строки по пробелам на список
        list_records = record.strip().split()
        # Сохранение фамилии
        name = list_records[1]
        # Сохранение инициалов
        initials = ''.join(rec[0]+'.' for rec in list_records[2:4])
        # Сохранение полного имени
        full_name = f"{name} {initials}"
        # Округление значения часов до ближайшего целого
        hours = round(float(list_records[-1]))
        # Условие, если запись о сотруднике есть, то часы складываются
        if full_name in disbalance:
            disbalance[full_name] += hours
        # В противном случае добавляется новая запись
        else:
            disbalance[full_name] = hours
    # Подсчет итоговых часов списания
    for name, total_hours in disbalance.items():
        disbalance[name] = total_hours - norm

    return disbalance

def write_result(disbalance: Dict[str, int], file_path: str) -> None:
    """
        Функция записывает результаты анализа дизбаланса в текстовый файл

        Params:
                disbalance - словарь с дизбалансом рабочего времени, где ключ - имя сотрудника,
                             значение - количество часов дизбаланса
                file_path  - путь к файлу с результатами

        Описание функции:
        Функция создает два словаря: один для сотрудников с отрицательным дизбалансом (недоработка) и один для сотрудников с положительным
        дизбалансом (переработка). Затем она записывает информацию о каждом сотруднике в файл, сначала тех, кто недоработал, в алфавитном
        порядке, затем тех, кто переработал, также в алфавитном порядке. Перед положительными значениями дизбаланса ставится знак '+'.
        """
    with open(file_path, 'w', encoding='utf-8') as file:
        # Создание словаря для сотрудников с отрицательным дизбалансом
        negative_balance = {k: v for k, v in disbalance.items() if v < 0}
        # Создание словаря для сотрудников с положительным дизбалансом
        positive_balance = {k: v for k, v in disbalance.items() if v > 0}
        # Запись в файл сотруников с отрицательным дизбалансом
        for name, hours in sorted(negative_balance.items(), key=lambda x: x[0]):
            file.write(f"{name} {hours}\n")
        # Запись в файл сотруников с положительным дизбалансом
        for name, hours in sorted(positive_balance.items(), key=lambda x: x[0]):
            file.write(f"{name} +{hours}\n")

def main():
    norm, records = download_file('report.txt')
    disbalance = find_disbalance(norm, records)
    write_result(disbalance, 'result.txt')

if __name__ == "__main__":
    main()