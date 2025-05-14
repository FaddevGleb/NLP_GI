import spacy

import tools

def Combos(ReadText, NLP, lang, ComboNumber):
    FilteredText = tools.TextPreparation.TextPreparation(ReadText, lang)
    ProcessedText = NLP(FilteredText)
    Lemmas = tools.Lemmatization.Lemmatization(ProcessedText)
    SortedText = tools.FrequencyCalc.FrequencyCalc(Lemmas)
    Combos = []
    for i in range(len(Lemmas) - (ComboNumber - 1)):
        Combo = tuple(Lemmas[i:i + ComboNumber])  # Tuple type set to be used with Counter later
        Combos.append(Combo)
    SortedCombos = tools.FrequencyCalc.FrequencyCalc(Combos)
    return SortedCombos

"""t = open("LDAdoc2.txt", "r", encoding="utf-8").read()
print(Combos(t, spacy.load("ru_core_news_lg"), "ru", 3))
"""