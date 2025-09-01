import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    telegram_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    oanda_token: str = os.getenv("OANDA_TOKEN", "")
    oanda_account_id: str = os.getenv("OANDA_ACCOUNT_ID", "")

settings = Settings()
