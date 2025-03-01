from spacy.attrs import LEMMA  # атрибут LEMMA нужен чтобы метод count_by считал все формы слов.
from NLPSelection import NLPSelection
"""
 NLPSelection - модуль и его одноимённая функция из репозитория нашего проекта. Нужен для выбора языковой модели.
 Все методы библиотеки Spacy наследуются(?) из NLPSelection. Для корректной работы нужно установить на 02.03.2025
 такие языковые модели на устройство как ru_core_news_lg и en_core_web_lg. 
"""

#Объект класса FrequencyCalc будет хранит в себе анализируемый текст, частотный словарь и используемую языковую модель.


class FrequencyCalc:
    def __init__(self, raw_text, model):
        self.__orig_text = raw_text
        self.__nlp = NLPSelection(model)
        self.__done_text = self.__nlp(self.__orig_text)
        self.__frequency_dict = self.__done_text.count_by(LEMMA)
    """
    Конструктор. В качестве параметра raw_text принимается любой текст,
    а в качестве параметра model - пока что только "en" (английский) и "ru" (русский)
    """

    def get_frequency(self, word):
        return self.__frequency_dict[self.__nlp.vocab.strings[word]]
    #Функция возвращает частоту появления слова(параметр word) в тексте в виде числа.

    def get_dict(self):
        return self.__frequency_dict
    #Функция возвращает словарь из пар в виде токен : частота появления.

    def get_orig(self):
        return self.__orig_text
    #Функция возвращает анализируемый текст.

    def get_nlp(self):
        return self.__nlp
    #Функция возвращает используемую языковую модель.
