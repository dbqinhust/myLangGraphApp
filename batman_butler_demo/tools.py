import base64
import mimetypes

from langchain_core.messages import HumanMessage

from .gemini_client import create_gemini_model


def extract_text(img_path: str) -> str:
    """Extract text from a local image file using Gemini vision."""
    try:
        with open(img_path, "rb") as image_file:
            image_bytes = image_file.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = mimetypes.guess_type(img_path)[0] or "image/png"
        model = create_gemini_model()
        response = model.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": (
                                "Extract all the text from this image. "
                                "Return only the extracted text, no explanations."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            },
                        },
                    ]
                )
            ]
        )

        return str(response.content).strip()
    except Exception as error:
        print(f"Error extracting text: {error}")
        return ""


def divide(a: int, b: int) -> float:
    """Divide a and b."""
    return a / b


TOOLS = [divide, extract_text]
