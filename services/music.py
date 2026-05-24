"""
Task 2.2 — Freedom Music API client
All 12 voice commands from the spec.
Point MUSIC_API_URL to mock server (localhost:9000) until real API is ready.
"""

import httpx
import config

BASE    = config.MUSIC_API_URL
HEADERS = {
    "Authorization": f"Bearer {config.MUSIC_DEVICE_TOKEN}",
    "X-Device-ID":   config.DEVICE_ID,
    "Content-Type":  "application/json",
}


def _post(path: str, body: dict = {}) -> dict:
    try:
        r = httpx.post(f"{BASE}{path}", json=body, headers=HEADERS, timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def _get(path: str) -> dict:
    try:
        r = httpx.get(f"{BASE}{path}", headers=HEADERS, timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ── 12 music commands ─────────────────────────────────────────────────────────

def play(shuffle: bool = True) -> str:
    _post("/api/v1/player/play", {"shuffle": shuffle, "device_id": config.DEVICE_ID})
    return "Включаю. Хорошего настроения."

def pause() -> str:
    _post("/api/v1/player/pause")
    return "Пауза."

def next_track() -> str:
    _post("/api/v1/player/next")
    return "Следующий."

def prev_track() -> str:
    _post("/api/v1/player/prev")
    return "Возвращаемся."

def volume(delta: int) -> str:
    _post("/api/v1/player/volume", {"delta": delta})
    direction = "Тише." if delta < 0 else "Громче."
    return direction

def play_genre(genre: str) -> str:
    _post("/api/v1/player/play", {"genre": genre, "device_id": config.DEVICE_ID})
    labels = {
        "jazz":      "Включаю джаз. Классика вечера.",
        "rock":      "Включаю рок. Держитесь.",
        "classical": "Включаю классику. Beethoven одобряет.",
    }
    return labels.get(genre, f"Включаю {genre}.")

def play_mood(mood: str) -> str:
    _post("/api/v1/player/play", {"mood": mood, "device_id": config.DEVICE_ID})
    labels = {
        "relaxed":   "Включаю расслабляющую подборку. Приятного вечера.",
        "energetic": "Поднимаем энергию.",
        "happy":     "Весёлую подборку запустил.",
        "focus":     "Режим концентрации включён.",
    }
    return labels.get(mood, f"Включаю подборку: {mood}.")

def play_lang(lang: str) -> str:
    _post("/api/v1/player/play", {"lang": lang, "device_id": config.DEVICE_ID})
    return "Английская подборка. Enjoy." if lang == "en" else f"Подборка на {lang}."

def shuffle() -> str:
    _post("/api/v1/player/shuffle")
    return "Перемешиваю плейлист."

def like(track_id: str = "current") -> str:
    _post("/api/v1/player/like", {"track_id": track_id})
    return "Добавлено. Хороший вкус."

def current_track() -> str:
    data = _get("/api/v1/player/current")
    if "error" in data:
        return "Не удалось получить информацию о треке."
    track  = data.get("track",  "Неизвестный трек")
    artist = data.get("artist", "Неизвестный артист")
    return f"Играет {track} — {artist}."

def stop() -> str:
    _post("/api/v1/player/stop")
    return "Остановил музыку."
