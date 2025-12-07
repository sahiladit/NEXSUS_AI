import requests
from bs4 import BeautifulSoup

def parse_crawled_data(results, name):
    extracted = []
    name_lower = name.lower()

    for entry in results:
        snippet = entry["snippet"].lower()
        score = snippet.count(name_lower)  # basic relevance match

        extracted.append({
            "url": entry["url"],
            "snippet": entry["snippet"],
            "score": score
        })

    return extracted
