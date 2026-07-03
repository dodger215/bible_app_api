from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

_client = None


def get_genai_client():
    """Lazily create and return a genai.Client instance.

    Raises RuntimeError if `GENAI_API_KEY` is not set.
    """
    global _client
    if _client is None:
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise RuntimeError("GENAI_API_KEY environment variable is not set")
        _client = genai.Client(api_key=api_key)
    return _client


def generate_response(prompt):
    client = get_genai_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
