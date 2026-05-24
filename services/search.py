"""
Task 1.4 — DuckDuckGo web search
Free, no API key required. Returns top-3 snippets as a plain string
ready to inject into the LLM context.
"""

from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 3) -> str:
    # Enrich currency queries with KZT context automatically
    enriched = _enrich_query(query)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(enriched, max_results=max_results))
        if not results:
            return "Поиск не дал результатов."
        return "\n".join(f"- {r['title']}: {r['body']}" for r in results)
    except Exception as e:
        return f"Поиск недоступен: {e}"


def _enrich_query(query: str) -> str:
    """Append context to make search more specific for Kazakhstan users."""
    q = query.lower()
    if any(k in q for k in ["курс доллара", "курс евро", "dollar rate", "exchange rate"]):
        if "kzt" not in q and "тенге" not in q:
            return query + " KZT казахстан сегодня"
    if any(k in q for k in ["погода", "weather"]) and "алмат" not in q:
        return query + " Алматы"
    return query


def needs_search(text: str) -> bool:
    """
    Quick heuristic: should we search the web for this query?
    True  → fresh data needed (currency, weather, news, today/now)
    False → LLM knows the answer (general knowledge, conversation)
    """
    SEARCH_TRIGGERS = [
        "курс", "курс доллара", "новости", "погода", "сейчас", "сегодня",
        "найди", "поищи", "последние", "актуальн",
        "weather", "news", "rate", "today", "right now", "latest", "current",
    ]
    t = text.lower()
    return any(kw in t for kw in SEARCH_TRIGGERS)
