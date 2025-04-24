import re
from collections import defaultdict
from urllib.parse import quote
from httpx import Client
from parsel import Selector
client = Client(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
        "verify": "false"
    },
    follow_redirects=True,
    http2=True,  # use HTTP/2
)

def parse_search_results(selector: Selector):
    """parse search results from google search page"""
    results = []
    for box in selector.xpath("//h1[contains(text(),'Search Results')]/following-sibling::div[1]/div"):
        print(box)
        title = box.xpath(".//h3/text()").get()
        url = box.xpath(".//h3/../@href").get()
        text = "".join(box.xpath(".//div[@data-sncf]//text()").getall())
        if not title or not url:
            print("no t or url")
            continue
        url = url.split("://")[1].replace("www.", "")
        results.append(title, url, text)
    return results
def scrape_search(query: str, page=1):
    """scrape search results for a given keyword"""
    # retrieve the SERP
    url = f"https://www.google.com/search?hl=en&q={quote(query)}" + (f"&start={10*(page-1)}" if page > 1 else "")
    print(f"scraping {query=} {page=}")
    results = defaultdict(list)
    print(results)
    response = client.get(url)
    assert response.status_code == 200, f"failed status_code={response.status_code}"
    # parse SERP for search result data
    selector = Selector(response.text)
    results["search"].extend(parse_search_results(selector))
    return dict(results)
def check_ranking(keyword: str, url_match: str, max_pages=3):
    """check ranking of a given url (partial) for a given keyword"""
    rank = 1
    for page in range(1, max_pages + 1):
        results = scrape_search(keyword, page=page)
        print(results)
        for (title, result_url, text) in results["search"]:
            if url_match in result_url:
                print(f"rank found:\n  {title}\n  {text}\n  {result_url}")
                return rank
            rank += 1
    return None

check_ranking(
    keyword="scraping instagram",
    url_match="scrapfly.com/blog/",
)