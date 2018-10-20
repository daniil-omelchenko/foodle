from google.appengine.ext import ndb

import requests
from services import auth
from models import Product, Account


def sync_products_for_account(account):
    token = auth.get_access_token(account)
    r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}'.format(account, token))


def save_product(product):
    Product(
        key=ndb.Key(Product, product.product_id, parent=ndb.Key(Account, product.account_id)),

    )
