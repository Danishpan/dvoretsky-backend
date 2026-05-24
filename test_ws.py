# test_ws.py — replace contents with this
import asyncio, websockets, json

TESTS = [
    {"text": "Дворецкий, привет",          "device_id": "test"},
    {"text": "включи джаз",                "device_id": "test"},
    {"text": "что сейчас играет",          "device_id": "test"},
    {"text": "следующий",                  "device_id": "test"},
    {"text": "тише",                       "device_id": "test"},
    {"text": "курс доллара сегодня",       "device_id": "test"},
    {"text": "включи что-нибудь весёлое",  "device_id": "test"},
]

async def test():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        for msg in TESTS:
            await ws.send(json.dumps(msg))
            reply = json.loads(await ws.recv())
            print(f"\n→ {msg['text']}\n← {reply['text']}")

asyncio.run(test())