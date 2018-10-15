from google.appengine.api import urlfetch
from telegram.ext import MessageHandler, filters

from main import app
from settings import settings


@app.handler(MessageHandler, filters=filters.Filters)
def default():
    c = urlfetch.fetch(
        'https://omelchenko.joinposter.com/api/menu.getProducts?token={}'.format(settings.POSTER_TEST_TOKEN)).content
    return c
