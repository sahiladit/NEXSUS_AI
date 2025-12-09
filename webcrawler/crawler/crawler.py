import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NexsusBot/1.0; +https://example.com/bot)"
}

def generate_seeds(name):
    cleaned = name.replace(" ", "+")
    return [
        f"https://duckduckgo.com/html/?q={cleaned}",
        f"https://www.bing.com/search?q={cleaned}",
        f"https://www.ask.com/web?q={cleaned}"
    ]


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
    text = soup.get_text(" ", strip=True)
    return " ".join(text.split()[:120])  # first 120 words


def generate_seeds(name):
    cleaned = name.replace(" ", "_")

    return [
        f"https://en.wikipedia.org/wiki/{cleaned}",
        f"https://about.me/{cleaned.replace('_','')}",
        f"https://github.com/{cleaned.replace('_','').lower()}",
        f"https://en.wikipedia.org/w/index.php?search={cleaned}",
    ]




def crawl_web(name, max_pages=10, depth=2):
    """
    Real webcrawler that:
    - Starts from seed URLs
    - BFS crawls outward
    - Extracts text data
    """

    # Seed sites we crawl manually
    seeds = generate_seeds(name)

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


