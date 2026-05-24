from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from routers.ws_handler import ws_endpoint
import config  # loads .env on import

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🎩 Дворецкий backend starting...")
    print(f"   Model : {config.GROQ_MODEL}")
    print(f"   Music : {config.MUSIC_API_URL}")
    yield
    print("Shutting down.")

app = FastAPI(title="Дворецкий Backend", version="1.0.0", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "dvoretsky-backend"}

@app.websocket("/ws")
async def websocket_route(ws: WebSocket):
    await ws_endpoint(ws)
