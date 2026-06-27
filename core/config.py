import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

AGENTOPS_API_URL = os.getenv("AGENTOPS_API_URL", "http://127.0.0.1:8000")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
