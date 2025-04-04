import spacy
from spacy.attrs import LEMMA  # атрибут LEMMA нужен чтобы метод count_by считал все формы слов.
from collections import Counter # Standard library utilized for frequency distribution

from NLPSelection import NLPSelection
"""
 NLPSelection - модуль и его одноимённая функция из репозитория нашего проекта. Нужен для выбора языковой модели.
 Все методы библиотеки Spacy наследуются(?) из NLPSelection. Для корректной работы нужно установить на 02.03.2025
 такие языковые модели на устройство как ru_core_news_lg и en_core_web_lg. 
"""

#Объект класса FrequencyCalc будет хранит в себе анализируемый текст, частотный словарь и используемую языковую модель.

def FrequencyCalc(raw_text):
    Text = Counter(raw_text)
    KeyWords = {word: freq for word, freq in Text.items() if freq >= 1}  # Calculating the frequency
    TextOutput = dict(sorted(KeyWords.items(), key=lambda x: x[1], reverse=True))  # Sorting keywords in reverse
    return TextOutput  # Returns dictionary

#print(FrequencyCalc("hand, Hand, feet", spacy.load("en_core_web_lg")))