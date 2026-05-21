import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import BOT_TOKEN
from handlers import (
    start,
    help_command,
    lang_callback,
    handle_text,
    handle_document
)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(lang_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🤖 Бот запущен! Нажми Ctrl+C чтобы остановить.")
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=["message", "callback_query"])
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())