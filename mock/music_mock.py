"""
Task 2.3 — Freedom Music mock server
Simulates the real Freedom Music API so Дворецкий works end-to-end
even when the real API is not available.

Run in a SEPARATE terminal:
    uvicorn mock.music_mock:app --port 9000

Then set in .env:
    MUSIC_API_URL=http://localhost:9000
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI(title="Freedom Music MOCK", version="1.0.0")

# ── In-memory player state ────────────────────────────────────────────────────
_state = {
    "playing": False,
    "track":   "So What",
    "artist":  "Miles Davis",
    "album":   "Kind of Blue",
    "genre":   "jazz",
    "mood":    None,
    "volume":  70,
    "shuffle": False,
}

DEMO_TRACKS = {
    "jazz":      ("So What",             "Miles Davis"),
    "rock":      ("Bohemian Rhapsody",   "Queen"),
    "classical": ("Moonlight Sonata",    "Beethoven"),
    "relaxed":   ("Gymnopédie No.1",     "Erik Satie"),
    "energetic": ("Eye of the Tiger",    "Survivor"),
    "happy":     ("Happy",               "Pharrell Williams"),
    "focus":     ("Experience",          "Ludovico Einaudi"),
    "default":   ("Blinding Lights",     "The Weeknd"),
}


# ── Models ────────────────────────────────────────────────────────────────────

class PlayRequest(BaseModel):
    genre:     str  = ""
    mood:      str  = ""
    lang:      str  = ""
    shuffle:   bool = False
    device_id: str  = ""

class VolumeRequest(BaseModel):
    delta: int = 0

class LikeRequest(BaseModel):
    track_id: str = "current"


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "freedom-music-mock"}


@app.post("/api/v1/player/play")
def mock_play(req: PlayRequest):
    _state["playing"] = True
    _state["shuffle"] = req.shuffle

    key = req.genre or req.mood or "default"
    track, artist = DEMO_TRACKS.get(key, DEMO_TRACKS["default"])
    _state["track"]  = track
    _state["artist"] = artist
    _state["genre"]  = req.genre or _state["genre"]
    _state["mood"]   = req.mood or None

    return {"status": "playing", "track": track, "artist": artist}


@app.post("/api/v1/player/pause")
def mock_pause():
    _state["playing"] = False
    return {"status": "paused"}


@app.post("/api/v1/player/stop")
def mock_stop():
    _state["playing"] = False
    return {"status": "stopped"}


@app.post("/api/v1/player/next")
def mock_next():
    # Rotate through demo tracks
    keys  = list(DEMO_TRACKS.keys())
    cur   = _state.get("genre", "default")
    idx   = keys.index(cur) if cur in keys else 0
    nxt   = keys[(idx + 1) % len(keys)]
    track, artist = DEMO_TRACKS[nxt]
    _state["track"]  = track
    _state["artist"] = artist
    _state["genre"]  = nxt
    return {"status": "skipped", "track": track, "artist": artist}


@app.post("/api/v1/player/prev")
def mock_prev():
    keys  = list(DEMO_TRACKS.keys())
    cur   = _state.get("genre", "default")
    idx   = keys.index(cur) if cur in keys else 0
    prv   = keys[(idx - 1) % len(keys)]
    track, artist = DEMO_TRACKS[prv]
    _state["track"]  = track
    _state["artist"] = artist
    _state["genre"]  = prv
    return {"status": "previous", "track": track, "artist": artist}


@app.post("/api/v1/player/volume")
async def mock_volume(request: Request):
    body = await request.json()
    delta = body.get("delta", 0)
    _state["volume"] = max(0, min(100, _state["volume"] + delta))
    return {"status": "ok", "volume": _state["volume"]}


@app.post("/api/v1/player/shuffle")
def mock_shuffle():
    _state["shuffle"] = not _state["shuffle"]
    return {"status": "ok", "shuffle": _state["shuffle"]}


@app.post("/api/v1/player/like")
async def mock_like(request: Request):
    body = await request.json()
    return {"status": "liked", "track_id": body.get("track_id", "current")}


@app.get("/api/v1/player/current")
def mock_current():
    return {
        "track":   _state["track"],
        "artist":  _state["artist"],
        "album":   _state.get("album", ""),
        "playing": _state["playing"],
        "volume":  _state["volume"],
    }
