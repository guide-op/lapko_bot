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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = " ".join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def send_test_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document="content/mytext.txt",
    )


async def unknown_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def main() -> None:
    load_dotenv()
    is_local_execution = os.getenv("RENDER") == "local"

    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    handlers = [
        CommandHandler("start", start),
        CommandHandler("caps", caps),
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
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
