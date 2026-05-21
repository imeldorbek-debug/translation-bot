import os
from dotenv import load_dotenv

load_dotenv()  # читает .env файл и загружает переменные

BOT_TOKEN = os.getenv("BOT_TOKEN")        # токен от @BotFather
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # ключ Gemini
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")

# Названия языков для промптов
LANG_PAIRS = {
    "en_ru": ("English", "Russian"),
    "ru_en": ("Russian", "English"),
    "ru_uz": ("Russian", "Uzbek"),
    "uz_ru": ("Uzbek", "Russian"),
    "uz_en": ("Uzbek", "English"),
    "en_uz": ("English", "Uzbek"),
}
