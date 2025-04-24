import requests
from bs4 import BeautifulSoup


class SEOParser:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def get_search_results(self, query, num=10):
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []

    def parse_seo_data(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            return {
                'title': soup.title.string if soup.title else None,
                'meta_description': soup.find('meta', attrs={'name': 'description'})['content']
                if soup.find('meta', attrs={'name': 'description'}) else None,
                'h1': [h1.text.strip() for h1 in soup.find_all('h1')],
                'canonical': soup.find('link', rel='canonical')['href']
                if soup.find('link', rel='canonical') else None,
                'og_tags': {tag['property']: tag['content']
                            for tag in soup.select('meta[property^="og:"]')}
            }
        except Exception as e:
            print(f"Ошибка парсинга {url}: {e}")
            return {}


# Пример использования
if __name__ == "__main__":
    API_KEY = "AIzaSyB40SP_foUVnWl6tTfKlI-N9-l1-W24Xec"
    SE_ID = "017576662512468239146:omuauf_lfve"

    parser = SEOParser(API_KEY, SE_ID)
    results = parser.get_search_results("SEO tools")

    for result in results:
        url = result['link']
        print(f"Анализируем: {url}")
        seo_data = parser.parse_seo_data(url)
        print(f"SEO данные:\n{seo_data}\n{'=' * 50}")