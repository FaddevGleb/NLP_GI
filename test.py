import regex # Regular expressions (to replace it with 're' see TextPreparation.FilterUserChoice == 'en' section)
import spacy # NLP (download instructions are printed out)""
import matplotlib.pyplot as PLT # Visual plotting (see comments in the PlottingTheGraph function)
import umap
import numpy as np
from collections import Counter
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

def TextPreparation (TextInput=r"ZALUPA.txt"):
    OnlyCyrillicText = regex.sub(r'[^а-яА-ЯёЁ0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015\u0306\u0308]+', '', TextInput)
    TextWithoutNewlines = regex.sub(r'[\r\n]+', ' ', OnlyCyrillicText) 
    TextWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', TextWithoutNewlines)
    TextWithoutMultipleSpaces = regex.sub(r'\s{2,}', ' ', TextWithoutHyphens)
    TextWithoutYo = TextWithoutMultipleSpaces.replace('ё', 'е') # ё
    TextWithoutYo = TextWithoutYo.replace('Ё', 'Е') # Ё
    TextWithoutYo = TextWithoutYo.replace('\u0435\u0308', 'е') # е with diaeresis
    TextOutput = TextWithoutYo.replace('\u0415\u0308', 'Е')
    return TextOutput

def NLP():
    NLP = spacy.load("ru_core_news_lg")
    return NLP

def Lemmatization(TextInput):
    Included = {"NOUN", "ADJ", "VERB", "ADV"}
    TextOutput = [token.lemma_ for token in TextInput if token.pos_ in Included]
    return TextOutput

def FrequencyCalc(TextInput): 
    print("Calculating the frequency...")
    Text = Counter(TextInput)
    KeyWords = {word: freq for word, freq in Text.items() if freq >= 1}
    print("Sorting file content...")
    TextOutput = dict(sorted(KeyWords.items(), key=lambda x: x[1], reverse=True))
    return TextOutput 

def Replacer(TextVectors):
    NewText = ''

    Vectors = [NLP(x.lemma_).vector for x in TextVectors]
    print('Vectors got')

    nn = NearestNeighbors(n_neighbors=2, metric='cosine')
    nn.fit(np.array(list(set(Vectors))))
    print('model fitted')

    for i, x in tqdm(enumerate(Vectors), total=len(Vectors), desc="Processing Vectors"):
        _, indices = nn.kneighbors([x], n_neighbors=2)
        most_similar_index = indices[0][1]
        NewText += str(TextVectors[most_similar_index])
    return NewText

def PlottingGraph(TextInput, TextVectors, color):
    #Настройка UMAP для понижения размерности
    Reducer = umap.UMAP(n_neighbors=3, min_dist=0.1, init='random', random_state=1, transform_seed=1)
    NewVectors = Reducer.fit_transform(np.array(TextVectors) + np.random.normal(0, 0.01, np.array(TextVectors).shape))
    #Настройка PCA для понижения размерности

    gmm = GaussianMixture(n_components=int(len(TextVectors)/5), covariance_type='full', random_state=42)
    gmm.fit(NewVectors)
    labels = gmm.predict(NewVectors)  # Предсказанные кластеры

    sns.scatterplot(x=NewVectors[:, 0], y=NewVectors[:, 1], s=100, color=color, hue=labels, palette="husl") 
    
    for i, word in enumerate(TextInput):
        if str(word) == 'хуй':
            print(NewVectors[i, 0], NewVectors[i, 1])
        PLT.text(NewVectors[i, 0], NewVectors[i, 1], word, fontsize=8, ha='center', va='bottom', color='black', alpha=0.8)
    

print('beginning')
NLP = NLP()
print('NLP done')

PLT.figure(figsize=(20, 10))

# for Text, color in zip(['дом.txt', 'радость.txt', 'печаль.txt'], ['green', 'red', 'blue']):
#     Text = open(Text, 'r', encoding='utf-8').read()
#     print('done')
#     FilteredText = TextPreparation(Text)
#     print('FilteredText done')
#     ProcessedText = NLP(FilteredText)
#     print('ProcessedText done')
#     Lemmas = Lemmatization(ProcessedText)
#     print('Lemmas done')
#     LemmaDocs = NLP(" ".join(Lemmas))
#     SortedText = FrequencyCalc(Lemmas)
#     SortedTextVectors = [token.vector for token in LemmaDocs]
#     print('SortedTextVectors done')
#     PlottingGraph(SortedText, SortedTextVectors, color, axes)
# PLT.show()

#Text = open('ConvertedPDF (2).txt', 'r').read()
Text = open('ZALUPA.txt', 'r', encoding='utf-8').read()
print('done')
FilteredText = TextPreparation(Text)
print('FilteredText done')
ProcessedText = NLP(FilteredText)
print('ProcessedText done')    
Lemmas = list(set(Lemmatization(ProcessedText)))
print('Lemmas done')
LemmaDocs = NLP(" ".join(Lemmas))
SortedTextVectors = [token.vector for token in LemmaDocs]
print('SortedTextVectors done')
PlottingGraph(LemmaDocs, SortedTextVectors, 'blue')
PLT.show()