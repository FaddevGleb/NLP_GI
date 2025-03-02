import os


def DependenciesModelsInstall():
    enCoreInstallCommand = "python -m spacy download en_core_web_lg"
    ruCoreInstallCommand = "python -m spacy download ru_core_news_lg"
    dependenciesInstall = "pip install -r dependencies.txt"
    res1 = os.system(enCoreInstallCommand)
    res2 = os.system(ruCoreInstallCommand)
    res3 = os.system(dependenciesInstall)
