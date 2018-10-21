# coding=utf-8
import datetime

import logging
from telegram.ext import MessageHandler, CommandHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from main import app, bot
from services import search

SHARE_LOCATION = 'Share Location'


def send_location_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(SHARE_LOCATION, request_location=True)]
        ],
        one_time_keyboard=True,
        resize_keyboard=True)


@app.handler(CommandHandler, command='start')
def start(update, user):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'Hi! Foodle here 👋 \n')
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'Share your loaction to get better results \n',
        reply_markup=send_location_markup())


@app.handler(RegexHandler, pattern=SHARE_LOCATION)
def menu(update, user):
    user.location_updated = datetime.datetime.now()
    user.lat = update.message.location.latitude
    user.lon = update.message.location.longitude
    user.put()
    bot.send_message(
        chat_id=update.message.chat_id,
        reply_markup=ReplyKeyboardRemove(),
        text=u'Thanks!')


@app.handler(MessageHandler, filters=Filters.text)
def default(update, user):
    search_request = update.message.text
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='searching...')
    searchResults = search.find_products(search_request)
    for result in searchResults:
        # type: SearchedProduct result
        bot.send_message(chat_id=chat_id, text=result.SearchedProduct + '\n')
        bot.send_photo(chat_id=chat_id, photo=result.image)
    # ToDo: add product information


@app.handler(MessageHandler, filters=Filters.location)
def location(update, user):
    user.lon = update.message.location.longitude
    user.lan = update.message.location.latitude
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'Thank you:) Use \\search command to find something tasty \n')


@app.handler(CommandHandler, command='search')
def search_products(update, user):
    logging.debug('saving location {}'.format(update.message.location))
    user.location_updated = datetime.datetime.now()
    user.lat = update.message.location.latitude
    user.lon = update.message.location.longitude
    user.put()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=u'What would you like to eat? \n')
