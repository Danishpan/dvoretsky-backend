"""
LLM integration via Groq (free tier).
Models: llama-3.1-8b-instant (fast) / mixtral-8x7b-32768 (better quality).
Free limits: ~14,400 req/day — more than enough for demo.
Get API key at: https://console.groq.com
"""

import config
from groq import Groq

DVORETSKY_PROMPT = """Ты — Дворецкий, голосовой AI-ассистент Freedom Station в Казахстане.
Говоришь на русском и английском языках.
Умный, лаконичный, с лёгким юмором. Как Альфред у Бэтмена — служишь, но с достоинством.
Никогда не говоришь длинных монологов. Ответ — максимум 2 предложения.
Не выдумываешь факты и не додумываешь цифры. Если данные предоставлены — используй только их.
Валюта по умолчанию — казахстанский тенге (KZT). Курс доллара = USD/KZT, не USD/RUB.
Определяешь язык пользователя автоматически и отвечаешь на нём же (RU или EN)."""

_client = Groq(api_key=config.GROQ_API_KEY)


def ask_llm(user_text: str, history: list[dict]) -> str:
    """Direct LLM call — for general conversation and Q&A."""
    messages = [
        {"role": "system", "content": DVORETSKY_PROMPT},
        *history,
        {"role": "user", "content": user_text},
    ]
    try:
        resp = _client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        err = str(e)
        if "429" in err:
            return "Секунду, перегружен. Попробуйте ещё раз."
        if "401" in err or "403" in err or "api_key" in err.lower():
            return "Ошибка: неверный GROQ_API_KEY. Проверьте переменные окружения."
        if "connection" in err.lower() or "network" in err.lower():
            return f"Ошибка сети: {type(e).__name__} — {err}"
        return f"Ошибка LLM ({type(e).__name__}): {err}"


def ask_llm_with_search(user_text: str, history: list[dict], search_results: str) -> str:
    """LLM call with web search context injected."""
    augmented = (
        f"ДАННЫЕ ИЗ ИНТЕРНЕТА (используй ТОЛЬКО эти цифры, не придумывай своих):\n"
        f"{search_results}\n\n"
        f"Вопрос пользователя: {user_text}\n"
        f"Ответь кратко — 1-2 предложения, используя данные выше."
    )
    return ask_llm(augmented, history)
