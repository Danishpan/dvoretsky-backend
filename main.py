from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from routers.ws_handler import ws_endpoint
from services.llm import active_provider
import config  # loads .env on import

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🎩 Дворецкий backend starting...")
    print(f"   LLM   : {active_provider()}")
    print(f"   Music : {config.MUSIC_API_URL}")
    yield
    print("Shutting down.")

app = FastAPI(title="Дворецкий Backend", version="1.0.0", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "dvoretsky-backend"}

@app.get("/status")
async def status():
    return {
        "llm_provider": active_provider(),
        "hf_model":     config.HF_MODEL,
        "hf_token_set": bool(config.HF_TOKEN),
        "groq_key_set": bool(config.GROQ_API_KEY),
        "music_api":    config.MUSIC_API_URL,
        "device_id":    config.DEVICE_ID,
    }

@app.websocket("/ws")
async def websocket_route(ws: WebSocket):
    await ws_endpoint(ws)
