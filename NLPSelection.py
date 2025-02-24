import spacy  # Импорт библиотеки spaCy для NLP задач


def NLPSelection(modelChoice, customModel=False):
    """
    Выбирает и загружает модель spaCy в зависимости от параметров.

    Параметры:
        modelChoice (str):
            - 'ru' для русской модели
            - 'en' для английской модели
            - имя кастомной модели (требует customModel=True)
        customModel (bool): Флаг использования кастомной модели

    Возвращает:
        nlp: Объект модели spaCy
        или -1 при неверных параметрах
    """

    # Загрузка русской модели с векторами слов (большая версия)
    if modelChoice == 'ru':
        return spacy.load("ru_core_news_lg")

        # Загрузка английской модели с векторами слов
    elif modelChoice == 'en':
        return spacy.load("en_core_web_lg")

        # Загрузка пользовательской модели по имени
    if customModel:
        return spacy.load(modelChoice)

    # Возврат ошибки при неверных параметрах
    else:
        return -1
