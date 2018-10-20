from google.appengine.ext import ndb

import requests

from domain.hook_update import HookUpdate, HookObject
from domain.product import Product

from services import auth, spots

from models import ProductModel, AccountModel


def sync_products_for_account(account):
    # type: (str) -> None
    token = auth.get_access_token(account)
    r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}'.format(account, token))
    products = map(Product.deserialize, r.json().get('response'))
    for product in products:
        save_product_to_account(product, account)


def get_product_for_account(product_id, account):
    # type: (str, str) -> Product
    token = auth.get_access_token(account)
    r = requests.get(
        'https://{}.joinposter.com/api/menu.getProduct?token={}&product_id={}'.format(account, token, product_id))
    return Product.deserialize(r.json().get('response'))


def save_product_to_account(product, account_id):
    # type: (Product, str) -> None
    ProductModel(
        key=ndb.Key(ProductModel, product.product_id, parent=ndb.Key(AccountModel, account_id)),
        product_name=product.product_name,
        product_id=product.product_id,
        photo_url='https://{}.joinposter.com'.format(account_id) + product.photo_url,
        price=product.price,
        category_name=product.category_name
    ).put()
    for spot in product.spots:
        spots.sync_spot(spot, account_id, product.product_id)



def update_by_hook(hook_update):
    # type: (HookUpdate) -> None
    if hook_update.object == HookObject.PRODUCT:
        product = get_product_for_account(hook_update.object_id, hook_update.account)
        save_product_to_account(product, hook_update.account)


def remove_for_account(account_name):
    product_models = ProductModel.get(parent=ndb.Key(AccountModel, account_name))
    while product_models:
        try:
            product_models.key.delete()
            product_models = ProductModel.get(parent=ndb.Key(AccountModel, account_name))
        except Exception:
            break