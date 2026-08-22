"""Client for looking up article summaries via the Wikimedia (MediaWiki) API."""

from __future__ import annotations

import httpx

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "cloud-gpt-physics-api/0.1 (https://github.com/deepaksaranay/cloud-gpt)"


def search_titles(query: str, client: httpx.Client, limit: int = 1) -> list[str]:
    """Search Wikipedia and return matching article titles, best match first."""
    response = client.get(
        API_URL,
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
        },
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    return [hit["title"] for hit in response.json()["query"]["search"]]


def get_summary(title: str, client: httpx.Client) -> dict:
    """Fetch the plain-text intro extract and canonical URL for a Wikipedia article."""
    response = client.get(
        API_URL,
        params={
            "action": "query",
            "prop": "extracts|info",
            "exintro": True,
            "explaintext": True,
            "inprop": "url",
            "titles": title,
            "format": "json",
        },
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    pages = response.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return {
        "title": page["title"],
        "extract": page.get("extract", "").strip(),
        "url": page.get("fullurl", f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"),
    }


def fetch_answer(query: str, client: httpx.Client | None = None) -> dict | None:
    """Look up the best-matching Wikipedia article summary for a question or topic.

    Returns None if Wikipedia has no matching article. Accepts an optional
    pre-configured client so callers (and tests) can inject their own transport.
    """
    owns_client = client is None
    client = client or httpx.Client(timeout=10.0)
    try:
        titles = search_titles(query, client)
        if not titles:
            return None
        return get_summary(titles[0], client)
    finally:
        if owns_client:
            client.close()
