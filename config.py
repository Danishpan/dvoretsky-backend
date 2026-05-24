import os
from dotenv import load_dotenv

load_dotenv()

# Hugging Face (primary)
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL  = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

# Groq (fallback if HF fails)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Freedom Music
MUSIC_API_URL      = os.getenv("MUSIC_API_URL", "http://localhost:9000")
MUSIC_DEVICE_TOKEN = os.getenv("MUSIC_DEVICE_TOKEN", "demo_token")

# Device
DEVICE_ID   = os.getenv("DEVICE_ID", "dvr_demo_001")
DEMO_MODE   = os.getenv("DEMO_MODE", "false").lower() == "true"

# Redis (optional)
REDIS_URL = os.getenv("REDIS_URL", "")
