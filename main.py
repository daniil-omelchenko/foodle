import logging

import requests
import telegram
from flask import Flask, request, redirect

from settings import settings
from utils.telegram_utils import handler
from models import User


Flask.handler = handler
app = Flask(__name__)
app.handler_registry = []
bot = telegram.Bot(settings.BOT_TOKEN)


# telegram bot update hook
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


# web hook for updating data for poster
@app.route('/webhook', methods=['POST'])
def poster_webhook():
    data = request.json

    return 'ok'


@app.route('/connect', methods=['GET'])
def connect_new_poster_account():
    auth_url = 'https://{}.joinposter.com/api/auth?application_id={}&redirect_uri={}&response_type=code'.format(
        request.args.get('poster_url'),
        settings.POSTER_APP_ID,
        settings.POSTER_REDIRECT_URI
    )
    return requests.get(auth_url).content


@app.route('/api/auth/login', methods=['GET', 'POST'])
def login():
    code = request.args.get('code')
    account = request.args.get('account')
    data = {
        'application_id': settings.POSTER_APP_ID,
        'application_secret': settings.POSTER_APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.POSTER_REDIRECT_URI,
        'code': code
    }
    r = requests.post('https://{}.joinposter.com/api/auth/access_token'.format(account), data=data)
    logging.debug(r.content)
    access_token = r.json().get('access_token')
    return 'WELCOME TO FOODLE! {}'.format(access_token)


@app.route('/welcome', methods=['GET'])
def welcome():
    return 'WELCOME TO FOODLE!'


@app.route('/menu', methods=['GET'])
def a():
    c = requests.get(
        'https://omelchenko.joinposter.com/api/menu.getProducts?token={}'.format(settings.POSTER_TEST_TOKEN))
    return c.content


import handlers