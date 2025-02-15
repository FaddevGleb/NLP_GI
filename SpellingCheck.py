from spellchecker import SpellChecker
import re


def SpellingCorrection(inputText, resname, lang):
    spellChecker = SpellChecker(language=lang)
    text = re.findall('[a-zа-яё]+', inputText, flags=re.IGNORECASE)
    processedText = []
    for word in text:
        correction = spellChecker.correction(word)
        if correction is not None:
            processedText.append(correction)
        else:
            processedText.append(word)
    writableText = " ".join(processedText)
    with open(f'{resname}.txt', mode='w') as f:
        f.write(writableText)

def FindMistakes(inputText, lang):
    spellChecker = SpellChecker(language=lang)
    text = re.findall('[a-zа-яё]+', inputText, flags=re.IGNORECASE)
    probableMistakes = spellChecker.unknown(text)
    mistakesCorrected = {}
    for word in probableMistakes:
        corrections = spellChecker.candidates(word)
        if corrections is not None:
            mistakesCorrected[word] = corrections
    return mistakesCorrected

"""
with open("ConvertedPDF.txt", "r") as f:
    tx = " ".join(f.readlines())
    print(FindMistakes(tx, "ru"))
"""