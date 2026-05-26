import os
import httpx
from typing import Any

async def start_bot(token: str):
    """Starts a simple Telegram bot that forwards messages to backend API.

    This is a lightweight example using `python-telegram-bot` Application.
    If you provide `TELEGRAM_TOKEN` the app will attempt to start polling.
    """
    try:
        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("Привет! Ваше сообщение будет отправлено в поддержку.")

        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = update.message.text or ""
            backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000/tickets/submit")
            async with httpx.AsyncClient() as client:
                await client.post(backend_url, json={"text": text})
            await update.message.reply_text("Спасибо, заявка принята.")

        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()
    except Exception:
        return
