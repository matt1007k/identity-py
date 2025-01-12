from dotenv import load_dotenv
import os

load_dotenv()

BROWSER_URL = os.getenv("BROWSER_URL")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
