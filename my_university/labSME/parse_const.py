input_file = 'D:/GitHub_projects/my_university/labSME/constants.txt'  # Имя вашего исходного файла
output_file = 'D:/GitHub_projects/my_university/labSME/const.py'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:

    for line in infile:
        line = line.strip()
        if not line or ' - ' not in line:
            continue  # Пропускаем пустые и некорректные строки

        # Разделяем строку на название переменной и значения
        var_name, values_str = line.split(' - ', 1)
        var_name = var_name.strip()

        # Извлекаем первое значение
        values = [v.strip() for v in values_str.split(';')]
        if not values:
            continue  # Нет значений для обработки
        first_value = values[0]

        py_value = float(first_value) # Сделали из строкового значения численное

        # Записываем результат в файл
        outfile.write(f"{var_name} = {py_value}\n")
