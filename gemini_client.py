import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def create_gemini_model() -> ChatGoogleGenerativeAI:
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(model=model_name, temperature=0)


def response_text(response: object) -> str:
    text = getattr(response, "text", None)
    if text:
        return text

    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("text")
        )

    return str(content)
