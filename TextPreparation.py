import regex  # Используется для расширенных возможностей Unicode (\p{})


def TextPreparation(TextInput, filterUserChoice="ru", latinUserChoice='n'):
    """
    Подготавливает текст для последующей обработки:
    - Фильтрует символы по языковому признаку
    - Нормализует пробелы и дефисы
    - Удаляет диакритические знаки

    Параметры:
    TextInput (str): Исходный текст для обработки
    filterUserChoice (str): Режим фильтрации ['ru'|'en'|'skip']
    latinUserChoice (str): Режим фильтрации латиницы ['yes'|'no'] (только для filterUserChoice='en')

    Возвращает:
    str: Очищенный и нормализованный текст

    Примеры вызова:
    TextPreparation(text, 'ru')        # Русский текст (по умолчанию)
    TextPreparation(text, 'en', 'y')   # Английский текст (базовая латиница)
    TextPreparation(text, 'skip')      # Без фильтрации символов
    """
    textOutput = None

    # Режим обработки русского текста
    if filterUserChoice == 'ru':
        # Основной фильтр: кириллица + базовые символы
        onlyCyrillicText = regex.sub(
            r'[^а-яА-ЯёЁ0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015\u0306\u0308]+',
            '',
            TextInput
        )

        # Унификация переносов строки
        textWithoutNewlines = regex.sub(r'[\r\n]+', ' ', onlyCyrillicText)

        # Нормализация дефисов (разные типы → стандартный '-')
        textWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', textWithoutNewlines)

        # Удаление двойных пробелов
        textWithoutMultipleSpaces = regex.sub(r'\s{2,}', ' ', textWithoutHyphens)

        # Замена буквы "ё" и комбинируемых символов
        textWithoutYo = (
            textWithoutMultipleSpaces
            .replace('ё', 'е')
            .replace('Ё', 'Е')
            .replace('\u0435\u0308', 'е')  # е с трема
            .replace('\u0415\u0308', 'Е')  # Е с трема
        )
        textOutput = textWithoutYo

    # Режим обработки английского текста
    elif filterUserChoice == 'en':
        # Выбор между базовой и расширенной латиницей
        if latinUserChoice:
            # Только ASCII-символы (A-Z, a-z)
            onlyLatinText = regex.sub(
                r'[^a-zA-Z0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015]+',
                '',
                TextInput
            )
        elif latinUserChoice:
            # Все символы категории Latin (включая диакритику)
            onlyLatinText = regex.sub(
                r'[^\p{Latin}0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015]+',
                '',
                TextInput
            )

        # Общие преобразования для английского текста
        textWithoutNewlines = regex.sub(r'[\r\n]+', ' ', onlyLatinText)
        textWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', textWithoutNewlines)
        textOutput = regex.sub(r'\s{2,}', ' ', textWithoutHyphens)

    # Режим без фильтрации символов
    elif filterUserChoice == 'skip':
        # Только базовая очистка (без языковой фильтрации)
        textWithoutNewlines = regex.sub(r'[\r\n]+', ' ', TextInput)
        textWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', textWithoutNewlines)
        textOutput = regex.sub(r'\s{2,}', ' ', textWithoutHyphens)

    return textOutput
