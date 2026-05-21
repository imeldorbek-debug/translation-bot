def get_translation_prompt(source_lang: str, target_lang: str, text: str) -> str:
    """
    Создаём инструкцию для Gemini.
    Чем точнее инструкция — тем лучше перевод.
    """
    return f"""You are an expert translator and highly educated engineer with deep knowledge \
of technical, scientific, and professional terminology in English, Russian, and Uzbek.

Your task: Translate the following text from {source_lang} to {target_lang}.

Rules:
- Translate with 100% accuracy — never guess, never paraphrase loosely
- Preserve all technical terms, units, formulas, brand names, and proper nouns correctly
- Keep the original formatting (line breaks, bullet points, numbering)
- If a technical term has no direct translation, keep the original and add a brief explanation in parentheses
- Use formal, professional register appropriate for engineering documents
- Do NOT add any commentary, explanation, or preamble — return ONLY the translated text

Text to translate:
{text}"""
