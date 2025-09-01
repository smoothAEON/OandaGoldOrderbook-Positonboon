from config.settings import settings
from bot.handlers import setup_bot
from oanda import OandaClient


def main() -> None:
    """Bootstrap configuration and start the bot."""
    if not settings.telegram_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    # Initialize Oanda client (not used yet)
    if settings.oanda_token:
        OandaClient(settings.oanda_token)

    application = setup_bot(settings.telegram_token)
    application.run_polling()


if __name__ == "__main__":
    main()
