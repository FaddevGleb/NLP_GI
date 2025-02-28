import requests

class SearchEngine:
    def __init__(self):
        self.API_KEY = 'AIzaSyDEty_zjHAqZifk0K0sitd02jy_7-Vn3wg'
        self.humanitarianAndSociologicalStudiesSearchAPIKey = '20837b3314fe541e7'
        self.allWebSearch = "71444b7ec7cd449e2"
        self.engines = [self.humanitarianAndSociologicalStudiesSearchAPIKey, self.allWebSearch]
        #Add more programmable search engines as need arises


    def getResultsByKeyword(self, query, engine):
        start = 1
        url = f"https://www.googleapis.com/customsearch/v1?key={self.API_KEY}&cx={self.engines[engine]}&q={query}&start={start}"
        data = requests.get(url).json()
        results = []
        for item in data['items']:
            """print(item['title'])
            print(item['link'])
            print(item['snippet'])
            print("========this is the result=========")"""
            results.append(tuple([item['title'], item['link'], item['snippet']]))
        return results

"""SE = SearchEngine()
print(SE.getResultsByKeyword("история", 1))
"""
