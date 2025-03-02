# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "scikit-learn",
#   "regex",
#   "spacy",
#   "matplotlib",
# ]
# ///

# Code is licensed under the Apache License 2.0
# Yury Leonidovich Samelik @ Moscow Polytechnic University
# E-mail: me@yurysamelik.ru
# 2024

from collections import Counter # Standard library utilized for frequency distribution
import sys # Standard library utilized to abort the script
import regex # Regular expressions (to replace it with 're' see TextPreparation.FilterUserChoice == 'en' section)
import spacy # NLP (download instructions are printed out)
import matplotlib.pyplot as PLT # Visual plotting (see comments in the PlottingTheGraph function)
from sklearn.decomposition import PCA # Vector dimensions reduction (see comments in the PlottingTheGraph function)

def TextPreparation(TextInput):
    'Preparing the raw text (important for Russian source data)'
    print("Select one of the options below regarding text processing...")
    print("ru: Leave only Cyrillic characters")
    print("en: Leave only Latin characters")
    print("skip: Do nothing and skip processing the text")
    print("Be aware: some Unicode symbols can mess up the output unless dealt with early on.")
    while True: # Running regular expressions to filter stuff
        FilterUserChoice = input("Your selection: ru/en/skip: ").strip().lower()
        if FilterUserChoice == 'ru': # Sample text of size 550000 is reduced to 500000
            print("Processing file content...")
            OnlyCyrillicText = regex.sub(r'[^а-яА-ЯёЁ0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015\u0306\u0308]+', '', TextInput) # Leaves only basic punctuation and Cyrillic characters
            TextWithoutNewlines = regex.sub(r'[\r\n]+', ' ', OnlyCyrillicText) # Replaces end-of-lines with spaces
            TextWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', TextWithoutNewlines) # Replaces some annoying hyphen variations with a regular one
            TextWithoutMultipleSpaces = regex.sub(r'\s{2,}', ' ', TextWithoutHyphens) # Replaces multiple spaces with a single space
            print("Replacing ё with e for congruity...")
            TextWithoutYo = TextWithoutMultipleSpaces.replace('ё', 'е') # ё
            TextWithoutYo = TextWithoutYo.replace('Ё', 'Е') # Ё
            TextWithoutYo = TextWithoutYo.replace('\u0435\u0308', 'е') # е with diaeresis
            TextOutput = TextWithoutYo.replace('\u0415\u0308', 'Е') # Е with diaeresis
            break # Exit the loop
        elif FilterUserChoice == 'en':
            print("Using the extended Latin characters set. Processing file content...")
            # OnlyLatinText is the only place where regex module is utilized (\p{Latin} character set)
            # Edit the loop below to leave only 'y' LatinUserChoice selection and replace 'import regex' with 'import re' in the header if you don't need this
            while True: # Leaving only basic Latin
                LatinUserChoice = input("Do you want to leave only basic latin (be aware: some words may have their individual letters removed)? (y/n): ").strip().lower()
                if LatinUserChoice == 'y':
                    OnlyLatinText = regex.sub(r'[^a-zA-Z0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015]+', '', TextInput) # Leaves only basic punctuation and basic Latin characters
                    # Alternative: text.encode("ASCII", "replace").decode()
                    break # Exits the loop
                elif LatinUserChoice == 'n':
                    OnlyLatinText = regex.sub(r'[^\p{Latin}0-9.,!?:\s\n\r\u002D\u2012\u2013\u2014\u2015]+', '', TextInput) # Leaves only basic punctuation and Latin characters
                    break # Exits the loop
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.") # Restarts the loop
            TextWithoutNewlines = regex.sub(r'[\r\n]+', ' ', OnlyLatinText) # Replaces end-of-lines with spaces
            TextWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', TextWithoutNewlines) # Replaces some annoying hyphen variations with a regular one
            TextOutput = regex.sub(r'\s{2,}', ' ', TextWithoutHyphens) # Replaces multiple spaces with a single space
            break # Exit the loop
        elif FilterUserChoice == 'skip':
            print("Skipping filtering the text...")
            TextWithoutNewlines = regex.sub(r'[\r\n]+', ' ', TextInput) # Replaces end-of-lines with spaces
            TextWithoutHyphens = regex.sub(r'[\u002D\u2012\u2013\u2014\u2015]+', '-', TextWithoutNewlines) # Replaces some annoying hyphen variations with a regular one
            TextOutput = regex.sub(r'\s{2,}', ' ', TextWithoutHyphens) # Replaces multiple spaces with a single space
            break # Exits the loop
        else:
            print("Invalid choice. Please enter 'ru' or 'en' or 'skip'.") # Restarts the loop
    print() # Print a blank line for readability
    return TextOutput # Returns string

def NLPSelection():
    'Choosing NLP model to use throughout the script'
    print("Please select which language model to use...")
    print("ru: SpaCy ru_core_news_lg (Russian)")
    print("en: SpaCy en_core_web_lg (English)")
    print("other: Enter SpaCy model name explicitly. Be aware that the script was tested only on Russian and English texts")
    print("abort: Stop the script")
    print("You may have to install the models separately using your preferred method.")
    print("Default download method is running 'python -m spacy download ru_core_news_lg' in your Python environment.")
    while True:
        NLPModelUserChoice = input("Your selection: ru/en/other/abort: ").strip().lower()
        if NLPModelUserChoice == 'ru':
            print("Russian model selected...")
            NLP = spacy.load("ru_core_news_lg") # Default 'lg' size option is included for use with word vectors later in the script
            break # Exits the loop
        elif NLPModelUserChoice == 'en':
            print("English model selected...")
            NLP = spacy.load("en_core_web_lg") # Default 'lg' size option is included for use with word vectors later in the script
            break # Exits the loop
        elif NLPModelUserChoice == 'other':
            CustomNLP = input("Please enter spaCy model name in a raw text format (no checks will be made): ").strip()
            NLP = spacy.load(CustomNLP)
            break # Exits the loop
        elif NLPModelUserChoice == 'abort':
            print("Aborting the script...")
            sys.exit(0) # Exits the script
        else:
            print("Invalid choice. Please enter either 'ru' or 'en' or 'other' or 'abort'.") # Restarts the loop
    print() # Print a blank line for readability
    return NLP

def Lemmatization(TextInput): # Accepts a spaCy doc object
    'Lemmatizes and optionally filters service parts of speech from the text'
    print("Select one of the following options regarding filtering the text...")
    print("y: Leave only nouns, adjectives, verbs, and adverbs")
    print("n: Filter nothing")
    print("choose: Enter the dialogue to filter only selected parts of speech")
    print("Be aware that language model may assign parts of speech tags somewhat randomly sometimes.")
    print("Also be aware that most of the time hyphens will be included as a category in the output regardless.")
    # By default we leave hyphens be because of the cases like 'well-known' and 'well known'
    # If you want to filter hyphens completely to clean the output you need to replace '-' with space in TextWithoutHyphens earlier in the script
    while True:
        FilterUserChoice = input("Your selection: y/n/choose: ").strip().lower()
        if FilterUserChoice == 'y':
            Included = {"NOUN", "ADJ", "VERB", "ADV"} # Nouns, adjectives, verbs, and adverbs
            TextOutput = [token.lemma_ for token in TextInput if token.pos_ in Included]
            break # Exits the loop
        elif FilterUserChoice == 'n':
            TextOutput = [token.lemma_ for token in TextInput] # Doesn't filter anything
            break # Exits the loop
        elif FilterUserChoice == 'choose':
            print("Now begins a series of queries regarding different parts of speech")
            print("Type 'y' if you want to filter current part of speech or press any key to skip")
            Excluded = set()
            if input("Do you want to filter pronouns? ").strip().lower() == 'y':
                Excluded.add("PRON") # Pronouns
            if input("Do you want to filter prepositions? ").strip().lower() == 'y':
                Excluded.add("ADP") # Prepositions
            if input("Do you want to filter determiners? ").strip().lower() == 'y':
                Excluded.add("DET") # Determiners
            if input("Do you want to filter particles? ").strip().lower() == 'y':
                Excluded.add("PART") # Particles
            if input("Do you want to filter auxilary verbs? ").strip().lower() == 'y':
                Excluded.add("AUX") # Auxilary verbs
            if input("Do you want to filter conjunctions? ").strip().lower() == 'y':
                Excluded.add("SCONJ") # Subordinatuing conjunctions
                Excluded.add("CCONJ") # Coordinations conjunctions
            if input("Do you want to filter symbols, numbers, and punctuation? ").strip().lower() == 'y':
                Excluded.add("SYM") # Symbols
                Excluded.add("PUNCT") # Punctuation
                Excluded.add("NUM") # Numbers
            TextOutput = [token.lemma_ for token in TextInput if token.pos_ not in Excluded] # Filters selected
            break # Exits the loop
        else:
            print("Invalid choice. Please enter either 'y' or 'n' or 'choose'.") # Restarts the loop
    print() # Print a blank line for readability
    return TextOutput # Returns list

def FrequencyCalc(TextInput): # Accepts a list
    'Calculating the frequency'
    print("Calculating the frequency...")
    while True: # Prompt the user for a threshold number
        try:
            UserThreshold = int(input("Please enter a threshold number (no results with a frequency lower than it will be shown): "))
            print(f"You entered the number: {UserThreshold}") # Gets the threshold
            break # Exits the loop
        except ValueError:
            print("Invalid input. Please enter a valid number.") # Restarts the loop
    Text = Counter(TextInput)
    KeyWords = {word: freq for word, freq in Text.items() if freq >= UserThreshold} # Calculating the frequency
    print("Sorting file content...")
    TextOutput = dict(sorted(KeyWords.items(), key=lambda x: x[1], reverse=True)) # Sorting keywords in reverse
    print() # Print a blank line for readability
    return TextOutput # Returns dictionary

def PlottingTheGraph(TextInput, TextVectors): # Accepts a dictionary and a list of Numpy arrays respectively
    'Plotting the data graph'
    # A very basic MatPlotLib plotting function
    # Produces relatively good results on small TextInput sizes
    # If you need the graph to be plotted with original word vectors but translated labels the best way would be to just translate the output manually
    # Supply the function with TextInput=TranslatedDictionary and TextVectors=OriginalVectors
    # Be aware that dictionary sizes need to be the same
    # Otherwise TranslatingTheOutput function is commented out later in the script
    print("Plotting the data graph...")
    PCAResult = PCA(n_components=2).fit_transform(TextVectors) # Reducing the dimensions of vectors
    PLT.figure(figsize=(10, 10))
    for i, word in enumerate(TextInput.keys()):
        PLT.scatter(PCAResult[i, 0], PCAResult[i, 1])
        PLT.text(PCAResult[i, 0], PCAResult[i, 1], word)
    print() # Print a blank line for readability
    PLT.show()

# Here's an output translation function using MyMemory free translation provider
# It produces relatively poor results thus it's currently deprecated
# MyMemory has a daily limit of about 5000 symbols so use if with caution if you enable it
# A better option to translate the output would be just do it manually
#
# from translate import Translator
# def TranslatingTheOutput (TextInput): # Add this function to FrequencyCalc() function output in the main body
#     TranslatedDictionary = {}
#     for word in TextInput.keys():
#         TranslatedWord = Translator(from_lang='ru', to_lang='en').translate(word) # Edit with desired language codes
#         TranslatedDictionary[TranslatedWord] = TextInput[word]
#     return TranslatedDictionary

def StoringTheResult(TextInput):
    'Printing or storing script output'
    print("Please choose one of the following options...")
    print("print: Print all of the results")
    print("top: Print only top 25")
    print("store: Store the output in a file")
    print("Script outputs its result it the format of 'Word:', 'Value:' pairs where value is either frequency or similarity.")
    print("Frequency is measured in number of occurances while similarity is measured in percent.")
    while True:
        StoringUserChoice = input("Your selection: print/top/store: ").strip().lower()
        if StoringUserChoice == 'print':
            print("Processed content: ")
            for word, value in TextInput.items():
                print(f'Word: {word}, Value: {value}')
            break # Exits the loop
        elif StoringUserChoice == 'top':
            print("Processed content (top 25): ")
            count = 0
            for word, value in TextInput.items():
                if count >= 25: # Could've been 50 or more but 25 is fine for the use case of many-word combos or heavily filtered text
                    break # Exits the loop
                print(f'Word: {word}, Value: {value}')
                count += 1
            break # Exits the loop
        elif StoringUserChoice == 'store':
            FilenameOutput = input("Enter the filename to store the result: ").strip()
            try:
                with open(FilenameOutput, 'w', encoding='utf-8') as fileout:
                    for word, value in TextInput.items():
                        fileout.write(f'Word: {word}, Value: {value}')
                        fileout.write('\n') # Ugly but gets the job done
                print(f"Result successfully stored in {FilenameOutput}.") # Doesn't indicate whether anything has been written for a case of an empty output
            except Exception as e:
                print(f"An error occurred while storing the result: {e}")
                sys.exit(1) # Exits the script
            break # Exits the loop
        else:
            print("Invalid choice. Please enter either 'print' or 'top' or 'store'.") # Restarts the loop

# Actual program starts here
# Introduction
print("Welcome to QuickNLPFreqTool: Basic Python NLP and Analysis Script v. 0.8.1.")
print("You can get an overview and version history on the Github page.")
print("The script will guide you through its process with different options mainly centered around Russian or English language models to use.")
print("Be aware that sometimes the script has to be run several times with different settings for you to get the desired output.")
print("Also note that while the script has been tested on Russian and English texts and various exceptions have been added it's not guaranteed to work every time.")
print() # Print a blank line for readability

# File input dialogue
print("Select a text file encoded with UTF-8.")
print("If later on you encounter an error specific to your input file try to edit the file first.")
print("You're free to edit the script as well obviously. Some possible settings to edit are discussed in the comments inside.")
FilenameInput = input("Please enter the filename to open: ") # Selecting the file to process
try:
    with open(FilenameInput, 'r', encoding='utf-8') as file: # Opening the file
        ReadText = file.read()
except FileNotFoundError:
    print("Error: File not found. Please check the filename and try again.")
    sys.exit(1) # Exits the script
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1) # Exits the script
print() # Print a blank line for readability

# Main body
print("Please choose one of the following options...")
print("words: Calculate the frequency of individual words")
print("combos: Process word combinations of selected length")
print("vectors: Use words vectors of a trained model to find similar words")
while True:
    ProcessingUserChoice = input("Your selection: words/combos/vectors: ").strip().lower()
    if ProcessingUserChoice == 'words': # Choice №1
        print() # Print a blank line for readability
        print("Proceeding with individual words...")
        FilteredText = TextPreparation(ReadText)
        NLP = NLPSelection()
        ProcessedText = NLP(FilteredText)
        Lemmas = Lemmatization(ProcessedText)
        SortedText = FrequencyCalc(Lemmas)
        StoringTheResult(SortedText)
        if input("Do you want to see word vectors of the script output in a handy graph? (y/n) ").strip().lower() == 'y':
            SortedTextVectors = [NLP(word).vector for word in SortedText] # List of Numpy arrays
            PlottingTheGraph(TextInput=SortedText, TextVectors=SortedTextVectors)
        print("Thank you for using QuickNLPFreqTool!")
        sys.exit(0) # Exits the script
    elif ProcessingUserChoice == 'combos': # Choice №2
        print() # Print a blank line for readability
        print("Proceeding with word combinations...")
        FilteredText = TextPreparation(ReadText)
        NLP = NLPSelection()
        ProcessedText = NLP(FilteredText)
        Lemmas = Lemmatization(ProcessedText)
        while True:
            try:
                ComboNumber = int(input("Please enter a combination number (e.g. 3 for 3-word combinations): "))
                print(f"You entered the number: {ComboNumber}") # Gets the combination length
                break # Exits the loop
            except ValueError:
                print("Invalid input. Please enter a valid number.") # Restarts the loop
        Combos = []
        for i in range(len(Lemmas) - (ComboNumber - 1)):
            Combo = tuple(Lemmas[i:i + ComboNumber]) # Tuple type set to be used with Counter later
            Combos.append(Combo)
        SortedCombos = FrequencyCalc(Combos)
        StoringTheResult(SortedCombos)
        print("Thank you for using QuickNLPFreqTool!")
        sys.exit(0) # Exits the script
    elif ProcessingUserChoice == 'vectors': # Choice №3
        print() # Print a blank line for readability
        print("Proceeding with word vectors...")
        FilteredText = TextPreparation(ReadText)
        NLP = NLPSelection()
        ProcessedText = NLP(FilteredText)
        Lemmas = Lemmatization(ProcessedText)
        SortedText = FrequencyCalc(Lemmas)
        SortedWords = NLP(' '.join(SortedText.keys())) # SpaCy needs to be applied on a string
        print("The script will now attempt to find words similar to the one you type in...")
        WordToFindSimilarTo = NLP(input("Enter the word in raw text format (no checks will be made): ").strip().lower())
        WordSimilarOutput = {}
        for word in SortedWords:
            if word.vector.any() != 0: # If there exists a vector for that word
                WordSimilarity = word.similarity(WordToFindSimilarTo)
                WordSimilarOutput[word] = WordSimilarity
        print("Sorting file content...")
        WordSimilarSorted = dict(sorted(WordSimilarOutput.items(), key=lambda x: x[1], reverse=True)) # Sorting vectors in reverse
        WordSimilar100Percent = {word: round(similarity * 100) for word, similarity in WordSimilarSorted.items()}
        print("Calculating the similarity...")
        while True: # Prompt the user for a similarity number
            try:
                SimilarityUserThreshold = int(input("Please enter a threshold number (no results with a similarity lower than it will be shown): "))
                print(f"You entered the number: {SimilarityUserThreshold}") # Gets the threshold
                break # Exits the loop
            except ValueError:
                print("Invalid input. Please enter a valid number.") # Restarts the loop
        WordSimilarThreshold = {word.text: freq for word, freq in WordSimilar100Percent.items() if freq >= SimilarityUserThreshold} # Calculating the frequency
        StoringTheResult(WordSimilarThreshold)
        if input("Do you want to present the results in a handy graph? (y/n) ").strip().lower() == 'y':
            top_words = dict(list(WordSimilarThreshold.items())[:25])
            top_vectors = [NLP(word).vector for word in top_words]
            PlottingTheGraph(TextInput=top_words, TextVectors=top_vectors)
        print("Thank you for using QuickNLPFreqTool!")
        sys.exit(0) # Exits the script
    else:
        print("Invalid choice. Please enter either 'words' or 'combos' or 'vectors'.") # Restarts the loop