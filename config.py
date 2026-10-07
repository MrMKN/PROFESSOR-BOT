import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", 0) or 0)
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
    BOT_SESSION = os.environ.get("BOT_SESSION", "mr_guardian_bot") 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    DATABASE_URI = os.environ.get("DATABASE_URI", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")
    BOT_OWNER = int(os.environ.get("BOT_OWNER", 0) or 0)
    FORWARD_SLEEP = float(os.environ.get("FORWARD_SLEEP", 1.8) or 1.8)
    CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "@moviesguardianss")

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
