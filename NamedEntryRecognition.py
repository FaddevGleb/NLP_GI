import pandas as pd
import spacy
import requests
from bs4 import BeautifulSoup

class NER:
    def __init__(self, model):
        self.model = spacy.load(model)

    def ner(self, content):
        doc = self.model(content)
        namedEntries = ""
        for ent in doc.ents:
            namedEntries += str(ent.text) + " " + str(ent.label_) + "\n"
            #print(str(ent.text), str(ent.label_))
        return namedEntries

"""
ner = NER("ru_core_news_lg")
with open("ConvertedPDF.txt", "r") as f:
    content = " ".join(f.readlines())
print(ner.ner(content))
"""