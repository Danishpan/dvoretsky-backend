"""
LLM integration — Hugging Face Inference API (primary, as per spec).
Automatic fallback to Groq if HF fails or rate-limits.

HF free tier models (1000 req/day):
  mistralai/Mistral-7B-Instruct-v0.3  ← default
  Qwen/Qwen2.5-7B-Instruct
  meta-llama/Llama-3.1-8B-Instruct

Token requires: "Make calls to Inference Providers" permission.
Get token at: https://huggingface.co/settings/tokens
"""

import config
from huggingface_hub import InferenceClient
from groq import Groq

DVORETSKY_PROMPT = """Ты — Дворецкий, голосовой AI-ассистент Freedom Station в Казахстане.
Говоришь на русском и английском языках.
Умный, лаконичный, с лёгким юмором. Как Альфред у Бэтмена — служишь, но с достоинством.
Никогда не говоришь длинных монологов. Ответ — максимум 2 предложения.
Не выдумываешь факты и не додумываешь цифры. Если данные предоставлены — используй только их.
Валюта по умолчанию — казахстанский тенге (KZT). Курс доллара = USD/KZT, не USD/RUB.
Определяешь язык пользователя автоматически и отвечаешь на нём же (RU или EN)."""

# Primary: Hugging Face
_hf_client = InferenceClient(
    model=config.HF_MODEL,
    token=config.HF_TOKEN,
) if config.HF_TOKEN else None

# Fallback: Groq
_groq_client = Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None


def _call_hf(messages: list[dict]) -> str:
    resp = _hf_client.chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


def _call_groq(messages: list[dict]) -> str:
    resp = _groq_client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


def ask_llm(user_text: str, history: list[dict]) -> str:
    messages = [
        {"role": "system", "content": DVORETSKY_PROMPT},
        *history,
        {"role": "user", "content": user_text},
    ]

    # Try HuggingFace first
    if _hf_client:
        try:
            return _call_hf(messages)
        except Exception as e:
            err = str(e)
            print(f"[HF error] {err} — falling back to Groq")
            if "429" in err:
                # HF rate limited — go straight to fallback
                pass
            elif "401" in err or "403" in err:
                print("[HF] Token permission error. Check 'Inference Providers' is enabled.")

    # Fallback: Groq
    if _groq_client:
        try:
            return _call_groq(messages)
        except Exception as e:
            err = str(e)
            if "429" in err:
                return "Секунду, перегружен. Попробуйте ещё раз."
            return f"Ошибка LLM ({type(e).__name__}): {err}"

    return "LLM не настроен. Проверьте HF_TOKEN или GROQ_API_KEY."


def ask_llm_with_search(user_text: str, history: list[dict], search_results: str) -> str:
    augmented = (
        f"ДАННЫЕ ИЗ ИНТЕРНЕТА (используй ТОЛЬКО эти цифры, не придумывай своих):\n"
        f"{search_results}\n\n"
        f"Вопрос пользователя: {user_text}\n"
        f"Ответь кратко — 1-2 предложения, используя данные выше."
    )
    return ask_llm(augmented, history)
