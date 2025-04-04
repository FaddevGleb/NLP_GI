import spacy

import tools

def VectorsPrecalc(ReadText, NLP, lang):
    FilteredText = tools.TextPreparation.TextPreparation(ReadText, lang)
    ProcessedText = NLP(FilteredText)
    Lemmas = tools.Lemmatization.Lemmatization(ProcessedText)
    SortedText = tools.FrequencyCalc.FrequencyCalc(Lemmas)
    SortedWords = NLP(' '.join(SortedText.keys()))
    return SortedWords

def Vectors(SortedWords, NLP, WordToFindSimilar):
    WordSimilarOutput = {}
    WordToFindSimilarTo = NLP(WordToFindSimilar.strip().lower())
    for word in SortedWords:
        if word.vector.any() != 0:  # If there exists a vector for that word
            WordSimilarity = word.similarity(WordToFindSimilarTo)
            WordSimilarOutput[word] = WordSimilarity
    WordSimilarSorted = dict(
        sorted(WordSimilarOutput.items(), key=lambda x: x[1], reverse=True))  # Sorting vectors in reverse
    WordSimilar100Percent = {word: round(similarity * 100) for word, similarity in WordSimilarSorted.items()}
    WordSimilarThreshold = {word.text: freq for word, freq in WordSimilar100Percent.items() if
                            freq >= 50}  # Calculating the frequency
    return WordSimilarThreshold

"""t = open("LDAdoc.txt", "r", encoding="utf-8").read()
print(VectorsPrecalc(t, spacy.load("ru_core_news_lg"), "ru"))
print(Vectors(VectorsPrecalc(t, spacy.load("ru_core_news_lg"), "ru"),spacy.load("ru_core_news_lg"), "Книга"))"""