import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    STRING_SESSION = os.getenv("STRING_SESSION")
    BOT_NAME = os.getenv("BOT_NAME")
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    BOT_GENDER = os.getenv("BOT_GENDER")
    REQUIRED_GROUP = os.getenv("REQUIRED_GROUP")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ACTIVE_AI = os.getenv("ACTIVE_AI")
