#!/bin/bash
# Starts both services inside one Railway container.
# Mock music server runs internally on :9000 (not public).
# Main backend runs on :8000 (Railway exposes this publicly).

echo "🎵 Starting Freedom Music mock server on :9000..."
uvicorn mock.music_mock:app --host 0.0.0.0 --port 9000 &

echo "🎩 Starting Дворецкий backend on :8000..."
uvicorn main:app --host 0.0.0.0 --port 8000
