import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are KnowledgeOS, a knowledge assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, clearly say that the information
is not available in the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text