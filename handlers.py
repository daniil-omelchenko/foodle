import logging

import telegram
from flask import request, redirect

import requests
from domain.hook_update import HookUpdate
from main import app, bot

from models import User

from services import auth, products
from services.settings import settings


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
    hook_update = HookUpdate.deserialize(data)
    token = auth.get_access_token(hook_update.account)
    products.update_by_hook(hook_update, token)
    return 'ok'


@app.route('/connect', methods=['GET'])
def connect_new_poster_account():
    auth_url = 'https://{}.joinposter.com/api/auth?application_id={}&redirect_uri={}&response_type=code'.format(
        request.args.get('poster_url'),
        settings.POSTER_APP_ID,
        settings.POSTER_REDIRECT_URI
    )
    return redirect(auth_url)


@app.route('/welcome', methods=['GET'])
def welcome():
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
    logging.debug(r.text)
    logging.debug(r.content)
    access_token = r.json().get('access_token')
    auth.save_account(account, access_token)
    return redirect('https://{}.joinposter.com/manage/applications/info/che-pozhevat'.format(account))


@app.route('/disconnect', methods=['GET'])
def disconnect():
    account = request.args.get('account_url')
    auth.delete_account(account)
    logging.debug(request.json)
    return redirect('https://{}.joinposter.com/manage/applications/info/che-pozhevat'.format(account))
