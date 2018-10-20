from google.appengine.ext import ndb

import domain.product
import requests
from services import auth
from models import Product, Account


def sync_products_for_account(account):
    token = auth.get_access_token(account)
    r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}'.format(account, token))


def save_product_to_account(product, account_id):
    # type: (domain.product.Product, str) -> None
    Product(
        key=ndb.Key(Product, product.product_id, parent=ndb.Key(Account, account_id)),
        product_name=product.product_name,
        product_id=product.product_id,
        photo_origin=product.photo_origin
    ).put()
