import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise EnvironmentError("Missing GROQ_API_KEY in environment")

    return Groq(api_key=api_key)