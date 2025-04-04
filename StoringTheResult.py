def StoringTheResult(TextInput, StoringUserChoice="print", filename="out.txt"):
    """Обрабатывает и сохраняет результаты анализа текста в зависимости от выбора пользователя.

    Параметры:
        TextInput (dict): Словарь формата {слово: численное_значение} (например, частота встречаемости)
        StoringUserChoice (str): Вариант обработки ('print', 'top', 'store')
        filename (str): Имя файла для сохранения (актуально при StoringUserChoice='store')

    Возвращает:
        list[tuple]/None/-1: Результаты в зависимости от режима:
            - print/top: список кортежей (слово, значение)
            - store: None при успехе, -1 при ошибке
    """

    # Режим 1: Полный вывод всех данных в виде списка кортежей
    if StoringUserChoice == 'print':
        allWordValues = []
        for word, value in TextInput.items():
            allWordValues.append(tuple([word, value]))  # Преобразуем каждую пару в кортеж
        return allWordValues

    # Режим 2: Вывод топ-25 элементов (предполагается, что словарь УЖЕ отсортирован)
    elif StoringUserChoice == 'top':
        topWordValues = []
        count = 0
        for word, value in TextInput.items():
            if count >= 25:  # Жёсткое ограничение количества элементов
                break
            topWordValues.append(tuple([word, value]))
            count += 1
        return topWordValues  # Если элементов меньше 25, вернёт все имеющиеся

    # Режим 3: Запись результатов в текстовый файл
    elif StoringUserChoice == 'store':
        try:
            with open(filename, 'w', encoding='utf-8') as fileout:
                for word, value in TextInput.items():
                    # Форматируем строку: "Word: {слово}, Value: {значение}\n"
                    fileout.write(f'Word: {word}, Value: {value}')
                    fileout.write('\n')  # Явное добавление переноса строки
            print(f"Result successfully stored in {filename}.")  # Уведомление в консоль
        except Exception as e:  # Широкий перехват исключений (пермиссий, диска и т.д.)
            return -1  # Возврат кода ошибки

