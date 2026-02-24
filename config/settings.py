# API Keys - GitHub Secrets theke nebe (safe)
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Languages
LANGUAGES = ["en", "bn"]  # English, Bangla

# Football Settings
LEAGUES = [
    {"id": 39, "name": "Premier League"},
    {"id": 140, "name": "La Liga"},
    {"id": 2, "name": "Champions League"},
    {"id": 135, "name": "Serie A"},
    {"id": 78, "name": "Bundesliga"},
]

# Video Settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30