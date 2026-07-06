import requests
from bs4 import BeautifulSoup
import time

BASE = "https://deep-forest-club.wikidot.com"
ARCHIVE = "https://web.archive.org/save/"

MAX_DEPTH = 3
MAX_PAGES = 150
visited = set()
queue = [(BASE, 0)]

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DeepArchiveBot/1.0)"
}

def archive(url):
    try:
        r = requests.get(ARCHIVE + url, headers=headers, timeout=60)
        print(f"{'✅' if r.status_code == 200 else '⚠️'} {url} ({r.status_code})")
    except Exception as e:
        print(f"❌ {url} -> {e}")

def crawl(url, depth):
    if depth > MAX_DEPTH or url in visited:
        return

    visited.add(url)
    archive(url)

    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            return

        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                full = BASE + href
            elif href.startswith(BASE):
                full = href
            else:
                continue

            if full not in visited:
                queue.append((full, depth + 1))
    except:
        pass

count = 0
while queue and count < MAX_PAGES:
    url, depth = queue.pop(0)
    crawl(url, depth)
    count += 1
    time.sleep(2)
