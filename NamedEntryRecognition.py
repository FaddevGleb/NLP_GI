import pandas as pd
import spacy
import requests
from bs4 import BeautifulSoup

def ner(content, model):
    doc = model(content)
    namedEntries = ""
    names = set()
    for ent in doc.ents:
        if ent.text not in names:
            namedEntries += str(ent.text) + " " + str(ent.label_) + "\n"
            names.add(ent.text)
        #print(str(ent.text), str(ent.label_))
    return namedEntries


"""ner = NER("en_core_web_lg")
with open("test.txt", "r") as f:
    content = " ".join(f.readlines())
print(ner.ner(content))"""
