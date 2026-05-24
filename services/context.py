"""
Task 1.5 — Dialogue context store
Keeps the last 10 conversation turns (20 messages) per device in memory.
No Redis needed for demo — swap the backend by editing only this file.
"""

from collections import defaultdict, deque

# device_id → deque of {"role": ..., "content": ...} dicts
_store: dict[str, deque] = defaultdict(lambda: deque(maxlen=20))


def get_history(device_id: str) -> list[dict]:
    """Return conversation history as a list (for passing to LLM messages)."""
    return list(_store[device_id])


def add_turn(device_id: str, user_text: str, assistant_text: str) -> None:
    """Append one user + assistant exchange."""
    _store[device_id].append({"role": "user",      "content": user_text})
    _store[device_id].append({"role": "assistant",  "content": assistant_text})


def clear_history(device_id: str) -> None:
    _store[device_id].clear()
