import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_product_links():

    response = requests.get(CATALOG_URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "product-catalog/view/" in href:

            if href.startswith("/"):
                href = BASE_URL + href

            links.add(href)

    return list(links)


def scrape_product(url):

    try:

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1")

        name = title.get_text(strip=True) if title else "Unknown"

        paragraphs = soup.find_all("p")

        description = " ".join([
            p.get_text(" ", strip=True)
            for p in paragraphs[:10]
        ])

        category = "Unknown"

        test_type = "Unknown"

        lower_desc = description.lower()

        if "personality" in lower_desc:
            category = "Personality"
            test_type = "P"

        elif "cognitive" in lower_desc:
            category = "Cognitive"
            test_type = "C"

        elif "technical" in lower_desc:
            category = "Technical"
            test_type = "K"

        elif "behavior" in lower_desc:
            category = "Behavioral"
            test_type = "B"

        return {
            "name": name,
            "url": url,
            "description": description,
            "category": category,
            "test_type": test_type
        }

    except Exception as e:

        print("Error scraping:", url)
        print(e)

        return None


def main():

    product_links = get_product_links()

    print(f"Found {len(product_links)} products")

    catalog = []

    for idx, url in enumerate(product_links):

        print(f"[{idx+1}/{len(product_links)}] Scraping")

        item = scrape_product(url)

        if item:
            catalog.append(item)

        time.sleep(0.5)

    with open("data/catalog.json", "w", encoding="utf-8") as f:

        json.dump(
            catalog,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nSaved {len(catalog)} products")


if __name__ == "__main__":
    main()