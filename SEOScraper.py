import requests

from bs4 import BeautifulSoup

def parse_reviews(url, type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    match type:
        case 0:
            results = soup.find_all("div", class_="otzivItem")
        case 1:
            results = soup.find_all("div", class_="font2")
    return results

def ParsePolytechData():
    results = []
    urls = ['https://vuzopedia.ru/vuz/5167/otziv', "https://tabiturient.ru/vuzu/mospolytech/"]
    for num, url in enumerate(urls):
        reviews = parse_reviews(url, num)
        for review in reviews:
            results.append(review.text)
    return results

print(ParsePolytechData())