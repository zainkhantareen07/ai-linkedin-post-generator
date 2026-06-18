import os
import sys
from dotenv import load_dotenv
import openai

# Setup path
sys.path.insert(0, os.path.dirname(__file__))


def get_openai_client():
    """Return configured `openai` module pointed at Grok (X.AI).

    This reads `XAI_API_KEY` from the environment (fallback to `GEMINI_API_KEY`).
    It sets `openai.api_key` and `openai.api_base` and returns the `openai` module
    so callers can use `client.ChatCompletion.create(...)`.
    """
    load_dotenv()

    key = os.getenv("XAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise EnvironmentError("Missing XAI_API_KEY (or GEMINI_API_KEY) in environment")

    openai.api_key = key
    # Point to Grok-compatible base
    openai.api_base = "https://api.x.ai/v1"

    return openai


if __name__ == "__main__":
    # Quick CLI test
    from generator import generate_post

    client = get_openai_client()
    topic = input("Enter a topic: ").strip()
    tone = input("Enter tone (professional/casual/viral): ").strip() or "professional"

    print("\nGenerating your LinkedIn post...\n")
    result = generate_post(topic, tone, client)

    print("HOOK:")
    print(result["hook"])
    print("\nPOST:")
    print(result["post"])
    print("\nCTA:")
    print(result["cta"])
    print("\nHASHTAGS:")
    print(" ".join(result["hashtags"]))
