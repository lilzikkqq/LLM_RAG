import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
CHROMA_PERSIST_PATH: str = os.getenv("CHROMA_PERSIST_PATH", "/app/chroma_db")
