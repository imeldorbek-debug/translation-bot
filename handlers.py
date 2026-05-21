from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from translator import translate_text
from file_handler import handle_pdf, handle_docx, handle_xlsx
from config import LANG_PAIRS
import os
import tempfile

# Кнопки выбора языка — показываются при /start
LANG_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇬🇧 EN → RU 🇷🇺", callback_data="en_ru"),
        InlineKeyboardButton("🇷🇺 RU → EN 🇬🇧", callback_data="ru_en"),
    ],
    [
        InlineKeyboardButton("🇷🇺 RU → UZ 🇺🇿", callback_data="ru_uz"),
        InlineKeyboardButton("🇺🇿 UZ → RU 🇷🇺", callback_data="uz_ru"),
    ],
    [
        InlineKeyboardButton("🇺🇿 UZ → EN 🇬🇧", callback_data="uz_en"),
        InlineKeyboardButton("🇬🇧 EN → UZ 🇺🇿", callback_data="en_uz"),
    ],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start — показываем приветствие и кнопки выбора языка"""
    await update.message.reply_text(
        "👋 Привет! Я бот-переводчик для технических текстов.\n\n"
        "Переводю точно, как опытный инженер.\n\n"
        "Выбери направление перевода:",
        reply_markup=LANG_BUTTONS
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help — инструкция"""
    await update.message.reply_text(
        "📖 Как пользоваться:\n\n"
        "1️⃣ Нажми /start и выбери направление перевода\n"
        "2️⃣ Отправь текст или файл (PDF, DOCX, XLSX)\n"
        "3️⃣ Получи точный технический перевод\n\n"
        "🌐 Языки: English 🇬🇧 · Русский 🇷🇺 · O'zbek 🇺🇿\n\n"
        "Чтобы сменить язык — нажми /start снова."
    )


async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Срабатывает когда пользователь нажимает на кнопку языка.
    Сохраняем выбор в context.user_data — это словарь для каждого пользователя отдельно.
    """
    query = update.callback_query
    await query.answer()  # убираем "часики" на кнопке

    lang_pair = query.data  # например "en_ru"
    source, target = LANG_PAIRS[lang_pair]

    # Сохраняем выбор пользователя
    context.user_data["source_lang"] = source
    context.user_data["target_lang"] = target

    await query.edit_message_text(
        f"✅ Выбрано: {source} → {target}\n\n"
        f"Отправь текст или файл (PDF, DOCX, XLSX) для перевода.\n"
        f"Чтобы сменить язык — нажми /start."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем обычный текст от пользователя"""
    if "source_lang" not in context.user_data:
        await update.message.reply_text(
            "⚠️ Сначала выбери направление перевода — нажми /start"
        )
        return

    source = context.user_data["source_lang"]
    target = context.user_data["target_lang"]
    text = update.message.text

    msg = await update.message.reply_text("⏳ Перевожу...")

    try:
        result = translate_text(text, source, target)
        await msg.edit_text(
            f"✅ *{source} → {target}*\n\n{result}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await msg.edit_text(f"❌ Ошибка: {str(e)}")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем файл (PDF, DOCX, XLSX)"""
    if "source_lang" not in context.user_data:
        await update.message.reply_text(
            "⚠️ Сначала выбери направление перевода — нажми /start"
        )
        return

    source = context.user_data["source_lang"]
    target = context.user_data["target_lang"]
    doc = update.message.document
    file_name = doc.file_name.lower()

    # Проверяем формат файла
    if not (file_name.endswith(".pdf") or
            file_name.endswith(".docx") or
            file_name.endswith(".xlsx")):
        await update.message.reply_text("❌ Поддерживаются только PDF, DOCX, XLSX")
        return

    msg = await update.message.reply_text("⏳ Скачиваю и обрабатываю файл...")

    try:
        # Скачиваем файл во временную папку
        file = await doc.get_file()
        suffix = os.path.splitext(file_name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            await file.download_to_drive(tmp.name)
            tmp_path = tmp.name

        await msg.edit_text("⏳ Перевожу содержимое файла...")

        # Выбираем нужный обработчик
        if file_name.endswith(".pdf"):
            output = handle_pdf(tmp_path, source, target)
        elif file_name.endswith(".docx"):
            output = handle_docx(tmp_path, source, target)
        elif file_name.endswith(".xlsx"):
            output = handle_xlsx(tmp_path, source, target)

        # Отправляем переведённый файл обратно
        await update.message.reply_document(
            document=open(output, "rb"),
            caption=f"✅ Переведено: {source} → {target}"
        )
        await msg.delete()

        # Удаляем временные файлы
        os.unlink(tmp_path)
        os.unlink(output)

    except Exception as e:
        await msg.edit_text(f"❌ Ошибка при обработке файла: {str(e)}")
