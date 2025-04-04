import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import umap
from sklearn.mixture import GaussianMixture
import tools
import spacy

def PlottingGraph(TextInput, TextVectors):
    matplotlib.use('Qt5Agg')
    print("enter")
    Reducer = umap.UMAP(n_neighbors=3, min_dist=0.1, init='random', random_state=1, transform_seed=1)
    print(0.5)
    NewVectors = Reducer.fit_transform(np.array(TextVectors) + np.random.normal(0, 0.01, np.array(TextVectors).shape))
    print("1")
    # Настройка кластеризации
    gmm = GaussianMixture(n_components=max(1, int(len(TextVectors) / 5)), covariance_type='full', random_state=42)
    gmm.fit(NewVectors)
    labels = gmm.predict(NewVectors)  # Предсказанные кластеры
    print(2)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=NewVectors[:, 0], y=NewVectors[:, 1], s=100, hue=labels, palette="husl")
    print(3)
    for i, word in enumerate(TextInput):
        plt.text(NewVectors[i, 0], NewVectors[i, 1], word, fontsize=8, ha='center', va='bottom', color='black', alpha=0.8)
    print(4)
    plt.savefig("graph.png", dpi=300, bbox_inches='tight')
    plt.show(block=False)
    plt.close()
    print(5)

"""Reducer = umap.UMAP(n_neighbors=3, min_dist=0.1, init='random', random_state=1, transform_seed=1)
"""
