from parsel import Selector
from urllib.parse import quote
from typing import List

client = httpx.Client(
    headers={
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    },
)

filecsv = open("seo_ranks.csv", "w", encoding="utf8")
csv_columns = ["keyword", "title", "text", "date", "domain", "url", "position"]
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()


def scrape_seo_ranks(keywords: List, max_pages: int):
    for keyword in keywords:
        position = 0
        # Iterate over Google search pages
        for page in range(1, max_pages + 1):
            print(f"scraping keyword {keyword} at page number {page}")

            url = f"https://www.google.com/search?hl=en&q={quote(keyword)}" + (
                f"&start={10*(page-1)}" if page > 1 else ""
            )
            request = client.get(url=url)
            selector = Selector(text=request.text)
            for result_box in selector.xpath(
                "//h1[contains(text(),'Search Results')]/following-sibling::div[1]/div"
            ):
                # Scrape search result boxes only
                try:
                    title = result_box.xpath(".//h3/text()").get()
                    text = "".join(
                        result_box.xpath(".//div[@data-sncf]//text()").getall()
                    )
                    date = text.split("—")[0] if len(text.split("—")) > 1 else "None"
                    url = result_box.xpath(".//h3/../@href").get()
                    domain = url.split("/")[2].replace("www.", "")
                    position += 1
                    writer.writerow(
                        {
                            "keyword": keyword,
                            "title": title,
                            "text": text,
                            "date": date,
                            "domain": domain,
                            "url": url,
                            "position": position,
                        }
                    )
                except:
                    pass

# Example use:
scrape_seo_ranks(["Web Scraping using Typescript", "Typescript web scraper"], 1)
