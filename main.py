import telegram
from flask import Flask

from utils.telegram_utils import handler
from services.settings import settings


Flask.handler = handler
app = Flask(__name__)
app.handler_registry = []
bot = telegram.Bot(settings.BOT_TOKEN)


import handlers
import bot_handlers
