import logging
import telegram
from flask import Flask, request

from settings import settings
from utils.telegram_utils import handler
from models import User


Flask.handler = handler
app = Flask(__name__)
app.handler_registry = []
bot = telegram.Bot(settings.BOT_TOKEN)


@app.route('/hook', methods=['POST'])
def hook():
    update = telegram.Update.de_json(request.json, bot)
    try:
        user = User.get_by_id(update.message.chat_id)
        if not user:
            user = User(
                id=update.message.chat_id,
                username=update.message.chat.username,
                first_name=update.message.chat.first_name,
                last_name=update.message.chat.last_name,
                type=update.message.chat.type,
            ).put()
        logging.info(request.json)
        for h in app.handler_registry:
            if h.check_update(update) and (not h.state or user.state == h.state):
                h.callback(update, user)
                break
    except Exception as ex:
        return 'fail'
    return 'ok'


import handlers