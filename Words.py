import spacy

import tools

def Words(ReadText, NLP, lang):
    FilteredText = tools.TextPreparation.TextPreparation(ReadText, lang)
    ProcessedText = NLP(FilteredText)
    Lemmas = tools.Lemmatization.Lemmatization(ProcessedText)
    SortedText = tools.FrequencyCalc.FrequencyCalc(Lemmas)
    return SortedText

"""with open("LDAdoc.txt", "r", encoding="utf-8") as f:
    print(Words(f.read(), spacy.load("ru_core_news_lg"), "ru"))"""