def Lemmatization(TextInput, stripChoice='no', excluded=None):
    """
    Производит лемматизацию текста с опциональной фильтрацией частей речи

    Параметры:
        TextInput (spacy.Doc): Объект документа spaCy для обработки
        stripChoice (str): Режим фильтрации:
            'no' - базовый фильтр (оставляет существительные, прилаг., глаголы, наречия)
            'yes' - без фильтрации (все токены)
            'select' - исключает части речи из параметра excluded
        excluded (set, optional): Множество тегов частей речи для исключения
                                (например: {'DET', 'ADP', 'PUNCT'})

    Возвращает:
        list: Список лемм/ -1 при некорректном режиме
    """

    # Базовый режим фильтрации: только смыслоносные части речи
    if stripChoice == 'no':
        # Включаемые категории (см. spaCy POS tagging)
        Included = {"NOUN", "ADJ", "VERB", "ADV"}
        TextOutput = [token.lemma_ for token in TextInput if token.pos_ in Included]

    # Режим без фильтрации - все токены
    elif stripChoice == 'yes':
        TextOutput = [token.lemma_ for token in TextInput]

    # Пользовательский режим исключений
    elif stripChoice == 'select':
        # Исключаем части речи из blacklist (требует передачи excluded)
        TextOutput = [token.lemma_ for token in TextInput if token.pos_ not in excluded]

    # Некорректный выбор режима
    else:
        return -1

    return TextOutput
