"""
WebSocket handler — receives {text, lang, device_id} from device,
routes through intent classifier, calls the right service, returns {text}.

Intent routing (Tasks 1.3–1.5):
  music  → services/music.py   (12 commands, mock server on :9000)
  search → DuckDuckGo + Groq LLM
  local  → datetime, no network
  llm    → Groq directly
"""

from fastapi import WebSocket, WebSocketDisconnect
import json, datetime

from services.intent   import classify
from services.llm      import ask_llm, ask_llm_with_search
from services.search   import web_search, needs_search
from services.context  import get_history, add_turn
import services.music as music


async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("📡 Device connected")

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "invalid json"}))
                continue

            text      = payload.get("text", "").strip()
            device_id = payload.get("device_id", "default")

            if not text:
                continue

            print(f"[{device_id}] → {text}")

            reply = dispatch(text, device_id)

            print(f"[{device_id}] ← {reply}")
            await websocket.send_text(json.dumps({"text": reply}))

    except WebSocketDisconnect:
        print("📡 Device disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


def dispatch(text: str, device_id: str) -> str:
    history = get_history(device_id)
    intent  = classify(text)

    if intent == "music":
        reply = route_music(text)

    elif intent == "search":
        snippets = web_search(text)
        reply    = ask_llm_with_search(text, history, snippets)

    elif intent == "local":
        reply = handle_local(text)

    else:  # "llm" — general conversation / Q&A
        reply = ask_llm(text, history)

    add_turn(device_id, text, reply)
    return reply


def route_music(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["стоп", "пауза", "stop", "pause"]):   return music.pause()
    if any(k in t for k in ["следующий", "next", "skip", "дальше"]): return music.next_track()
    if any(k in t for k in ["предыдущий", "назад", "previous", "back"]): return music.prev_track()
    if "тише"   in t or "quieter" in t: return music.volume(-15)
    if "громче" in t or "louder"  in t: return music.volume(+15)
    if "играет" in t or "what's playing" in t: return music.current_track()
    if "джаз"   in t or "jazz"    in t: return music.play_genre("jazz")
    if "рок"    in t or "rock"    in t: return music.play_genre("rock")
    if "классика" in t or "classical" in t: return music.play_genre("classical")
    if any(k in t for k in ["расслаб", "relax", "chill"]):   return music.play_mood("relaxed")
    if any(k in t for k in ["энерг",   "energy", "energetic"]): return music.play_mood("energetic")
    if any(k in t for k in ["весёл",   "happy",  "fun"]):    return music.play_mood("happy")
    if any(k in t for k in ["работ",   "focus",  "концентр"]): return music.play_mood("focus")
    if "english" in t or "английск" in t: return music.play_lang("en")
    return music.play()  # default: just play something


def handle_local(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["час", "время", "time"]):
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Сейчас {now}."
    return "Эта команда доступна офлайн."
