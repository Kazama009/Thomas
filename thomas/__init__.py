import os 
import time
import asyncio
import logging

from dotenv import load_dotenv

from telegram.ext import Application


logging.basicConfig(
    format="%(asctime)s - Thomas - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

try: 
    from config import Development as Config
except:
    LOGGER.info("Cannot import Config! Using ENV vars")

load_dotenv()

ENV = bool(os.environ.get("ENV", False))
START_TIME = time.time()

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    OPENAI_API_TOKEN = os.environ.get("OPENAI_API_TOKEN", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)

else:
    TOKEN = Config.TOKEN
    OPENAI_API_TOKEN = Config.OPENAI_API_TOKEN
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)

application = Application.builder().token(TOKEN).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())