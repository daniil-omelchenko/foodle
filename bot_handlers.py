# coding=utf-8
from telegram.ext import MessageHandler, CommandHandler, Filters

from main import app, bot


@app.handler(CommandHandler, command='start')
def start(update, user):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'Hi! Foodle here 👋 \n')


@app.handler(MessageHandler, filters=Filters.text)
def default(update, user):
    search_request = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text='searching...')
