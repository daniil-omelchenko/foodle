from google.appengine.ext import ndb

import requests

from domain.hook_update import HookUpdate, HookObject, HookAction
from domain.product import Product

from services import spots

from models import ProductModel, AccountModel


def sync_products_for_account(account, token):
    # type: (str) -> None
    r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}'.format(account, token))
    products = map(Product.deserialize, r.json().get('response'))
    for product in products:
        save_product_to_account(product, account, token)


def get_product_for_account(product_id, account, token):
    # type: (str, str) -> Product
    r = requests.get(
        'https://{}.joinposter.com/api/menu.getProduct?token={}&product_id={}'.format(account, token, product_id))
    return Product.deserialize(r.json().get('response'))


def save_product_to_account(product, account_id, token):
    # type: (Product, str) -> None
    ProductModel(
        key=ndb.Key(ProductModel, product.product_id, parent=ndb.Key(AccountModel, account_id)),
        product_name=product.product_name,
        product_id=product.product_id,
        photo_url='https://{}.joinposter.com'.format(account_id) + product.photo_url,
        category_name=product.category_name
    ).put()
    for spot in product.spots:
        spots.sync_spot(spot, account_id, product.product_id, token)


def remove_product(product_id, account):
    ndb.Key(ProductModel, product_id, parent=ndb.Key(AccountModel, account)).delete()


def update_by_hook(hook_update, token):
    # type: (HookUpdate) -> None
    if hook_update.object == HookObject.PRODUCT:
        product = get_product_for_account(hook_update.object_id, hook_update.account, token)
        if hook_update.action == HookAction.CHANGED:
            save_product_to_account(product, hook_update.account, token)
        elif hook_update.action == HookAction.ADDED:
            save_product_to_account(product, hook_update.account, token)
        elif hook_update.action == HookAction.REMOVED:
            remove_product(hook_update.object_id, hook_update.account)


def remove_for_account(account_name):
    product_ids = ProductModel.allocate_ids(parent=ndb.Key(AccountModel, account_name), max=1000)  # fixme later
    ndb.delete_multi(product_ids)
