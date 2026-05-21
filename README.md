# Translation Bot

A Telegram bot that translates technical texts between English, Russian, and Uzbek using the Gemini API.

## Features

- Translates plain text messages
- Translates documents: PDF, DOCX, XLSX
- Supports 6 language pairs: EN↔RU, RU↔UZ, UZ↔EN
- Preserves technical terminology and formatting

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your keys:
   ```
   BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Getting API keys

- **Telegram token**: create a bot via [@BotFather](https://t.me/BotFather)
- **Gemini key**: get one at [Google AI Studio](https://aistudio.google.com/)
