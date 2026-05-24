"""
Task 1.2 / 2.1 — Intent classifier
Rules-based keyword matching. Fast, no LLM call needed.
Returns one of: "music" | "search" | "local" | "llm"
"""

MUSIC_KW = [
    "включи", "поставь", "запусти", "play", "skip", "next",
    "pause", "стоп", "пауза", "тише", "громче", "следующий",
    "предыдущий", "джаз", "рок", "классика", "настроение",
    "что играет", "играет", "what's playing", "добавь в избранное",
    "расслаб", "энерг", "весёл", "работ", "focus", "chill",
    "english", "английск", "перемешай", "shuffle",
]

SEARCH_KW = [
    "курс", "новости", "погода", "сейчас", "сегодня",
    "найди", "поищи", "последние", "актуальн",
    "weather", "news", "rate", "today", "right now", "latest",
]

LOCAL_KW = [
    "который час", "сколько времени", "what time",
    "будильник", "напомни", "alarm", "статус", "status",
]


def classify(text: str) -> str:
    t = text.lower()
    if any(kw in t for kw in MUSIC_KW):  return "music"
    if any(kw in t for kw in SEARCH_KW): return "search"
    if any(kw in t for kw in LOCAL_KW):  return "local"
    return "llm"
