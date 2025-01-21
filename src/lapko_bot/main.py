import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.lapko_bot.quotify import fix

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Привіт! Я Лапко, і в мене лапки! 🐾 Напиши мені текст, і я спробую"
            " привести в ньому до ладу лапки та тире."
        ),
    )


async def reply_with_fix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=fix(update.message.text)
    )


async def unknown_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Га?",
    )


def main() -> None:
    load_dotenv()
    is_local_execution = os.getenv("RENDER") == "local"

    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    handlers = [
        CommandHandler("start", start),
        MessageHandler(filters.TEXT & (~filters.COMMAND), reply_with_fix),
        MessageHandler(filters.COMMAND, unknown_cmd),
    ]

    for handler in handlers:
        application.add_handler(handler)

    # Render webservices need to listen on a port. Otherwise, they auto-close.
    # Background workers don't need to do that. But they are paid.
    # Looking back, render might have been not the best choice for this project.
    # But, hey, at least it's free. And it works.
    if is_local_execution:
        application.run_polling()
    else:
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT")),
            secret_token=os.getenv("WEBHOOK_TOKEN"),
            webhook_url=os.getenv("RENDER_EXTERNAL_URL"),
        )


if __name__ == "__main__":
    main()
