from dotenv import load_dotenv
import os

load_dotenv()

BROWSER_URL = os.getenv("BROWSER_URL") or "http://127.0.0.1:4444"
REDIS_HOST = os.getenv("REDIS_HOST") or "127.0.0.1"
REDIS_PORT: int = int(os.getenv("REDIS_PORT") or "6379")
