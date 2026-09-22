from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from ddgs.exceptions import DDGSException


def _fallback_search(query, max_results=20):
    url = "https://duckduckgo.com/html/?q=" + quote_plus(query)
    try:
        response = requests.get(url, timeout=12, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        })
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for link in soup.select("a.result__a")[:max_results]:
        href = link.get("href")
        title = link.get_text(" ", strip=True)
        if href:
            results.append({"title": title, "href": href})
    return results


def search_web(query, max_results=20):
    if not query or not str(query).strip():
        return []

    try:
        with DDGS() as ddgs:
            return list(ddgs.text(str(query), max_results=max_results))
    except DDGSException:
        return _fallback_search(str(query), max_results=max_results)
    except Exception:
        return _fallback_search(str(query), max_results=max_results)
