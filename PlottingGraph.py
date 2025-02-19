def PlottingGraph(TextInput, TextVectors):
    #Настройка UMAP для понижения размерности
    Reducer = umap.UMAP(n_neighbors=3, min_dist=0.1, init='random', random_state=1, transform_seed=1)
    NewVectors = Reducer.fit_transform(np.array(TextVectors) + np.random.normal(0, 0.01, np.array(TextVectors).shape))
    
    #Настройка кластеризации
    gmm = GaussianMixture(n_components=int(len(TextVectors)/5), covariance_type='full', random_state=42)
    gmm.fit(NewVectors)
    labels = gmm.predict(NewVectors)  # Предсказанные кластеры

    sns.scatterplot(x=NewVectors[:, 0], y=NewVectors[:, 1], s=100, hue=labels, palette="husl") 
    for i, word in enumerate(TextInput):
        PLT.text(NewVectors[i, 0], NewVectors[i, 1], word, fontsize=8, ha='center', va='bottom', color='black', alpha=0.8)
    
    PLT.show()
