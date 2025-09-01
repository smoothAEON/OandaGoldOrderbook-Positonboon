from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if update.message:
        await update.message.reply_text("Hello! I'm a bot.")


def setup_bot(token: str) -> Application:
    """Create the Telegram application and register handlers."""
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    return application
