from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
from random import randint as rnd
import OCR

class ThematicAnalysis:

    def __init__(self, max_features, lang):
        self.countVectorizer = CountVectorizer(max_features=max_features, stop_words=lang)
        self.tfIdVectorizer = TfidfVectorizer(max_features=1000, stop_words='english')


    def RunLDA(self, document, num_topics=5):
        X = self.countVectorizer.fit_transform(document)
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=rnd(1, 100), max_iter=100)
        lda.fit(X)
        modelAnswer = ""
        for topic_idx, topic_words in enumerate(lda.components_):
            top_words_idx = topic_words.argsort()[-10:][::-1]
            top_words = [self.countVectorizer.get_feature_names_out()[i] for i in top_words_idx]
            modelAnswer += f"Тема {topic_idx + 1}: {', '.join(top_words)}\n"
        return modelAnswer

    def RunNMF(self, document, num_topics=5):
        nmf = NMF(n_components=num_topics, random_state=rnd(1, 50))
        X = self.tfIdVectorizer.fit_transform(document)
        nmf.fit(X)
        modelAnswer = ""
        feature_names = self.tfIdVectorizer.get_feature_names_out()
        for topic_idx, topic_words in enumerate(nmf.components_):
            top_words_idx = topic_words.argsort()[-15:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            modelAnswer += f"Тема {topic_idx + 1}: {', '.join(top_words)}\n"
        return modelAnswer

ocr = OCR.OCR("D:/NLP_GI/Tesseract-OCR/tesseract.exe")
ocr.ConvertPDF("rus", "LDA1.pdf", "LDAdoc")
ocr.ConvertPDF("rus", "LDA2.pdf", "LDAdoc2")
lda1 = open("LDAdoc.txt", "r")
lda2 = open("LDAdoc2.txt", "r")
tx = [" ".join(lda1.readlines()), " ".join(lda2.readlines())]
lda1.close()
lda2.close()
#tx = ["In accordance with the law the death sentence was announced to Cincinnatus C. in a whisper. All rose, exchanging smiles. The hoary judge put his mouth close to his ear, panted for a moment, made the announcement and slowly moved away, as though ungluing himself. Thereupon Cincinnatus was taken back to the fortress. The road wound around its rocky base and disappeared under the gate like a snake in a crevice. He was calm; however, he had to be supported during the journey through the long corridors, since he planted his feet unsteadily, like a child who has just learned to walk, or as if he were about to fall through like a man who has dreamt that he is walking on water only to have a sudden doubt: but is this possible? Rodion, the jailer, took a long time to unlock the door of Cincinnatus’ cell—it was the wrong key—and there was the usual fuss. At last the door yielded. Inside, the lawyer was already waiting."]
anal = ThematicAnalysis(100, "english")
print(anal.RunLDA(tx, 2))
print("-"*100)
print(anal.RunNMF(tx))
