from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import get_translation_prompt

client = genai.Client(api_key=GEMINI_API_KEY)

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if not text.strip():
        return ""

    prompt = get_translation_prompt(source_lang, target_lang, text)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text.strip()
