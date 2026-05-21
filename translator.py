import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import get_translation_prompt

genai.configure(api_key=GEMINI_API_KEY)

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if not text.strip():
        return ""

    prompt = get_translation_prompt(source_lang, target_lang, text)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()
