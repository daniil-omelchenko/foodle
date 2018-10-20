# coding=utf-8
import logging

import requests
from telegram.ext import MessageHandler, CommandHandler, Filters

from main import app, bot, settings


@app.handler(CommandHandler, command='start')
def start(update, user):
    logging.debug('HI')
    # c = requests.get('https://omelchenko.joinposter.com/api/menu.getProducts?token={}'.format(settings.POSTER_TEST_TOKEN))
    # logging.info(c.content)
    # bot.send_message(chat_id=update.message.chat_id, text=c.content[:100])
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'Hi! Foodle here 👋 \n')


@app.handler(MessageHandler, filters=Filters.text)
def default(update, user):
    c = requests.get(
        'https://omelchenko.joinposter.com/api/menu.getProducts?token={}'.format(settings.POSTER_TEST_TOKEN)).content
    logging.info(c)

    bot.send_message(chat_id=update.message.chat_id, text=c)


c = requests.get('https://omelchenko.joinposter.com/api/menu.getProducts?token={}'.format(POSTER_TEST_TOKEN))