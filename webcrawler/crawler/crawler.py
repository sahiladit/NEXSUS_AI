import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NexsusBot/1.0; +https://example.com/bot)"
}

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def extract_links(base_url, soup):
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if is_valid_url(full_url):
            links.add(full_url)
    return links

def extract_text(soup):
    paragraphs = soup.find_all("p")
    return " ".join(p.get_text(strip=True) for p in paragraphs[:10])

def crawl_web(name, max_pages=10, depth=2):
    """
    Real webcrawler that:
    - Starts from seed URLs
    - BFS crawls outward
    - Extracts text data
    """

    # Seed sites we crawl manually
    seeds = [
        f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}",
        f"https://linkedin.com/in/{name.replace(' ', '').lower()}",
        f"https://github.com/{name.replace(' ', '').lower()}",
        f"https://about.me/{name.replace(' ', '').lower()}",
        f"https://twitter.com/{name.replace(' ', '').lower()}"
    ]

    visited = set()
    queue = [(url, 0) for url in seeds]
    results = []

    while queue and len(results) < max_pages:
        url, level = queue.pop(0)

        if url in visited or level > depth:
            continue

        visited.add(url)

        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "lxml")
            text = extract_text(soup)

            if text.strip():
                results.append({
                    "url": url,
                    "snippet": text[:500]  # first 500 chars
                })

            # Add more links to queue
            for link in extract_links(url, soup):
                if link not in visited:
                    queue.append((link, level + 1))

        except Exception:
            continue

    return results


