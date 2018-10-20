from google.appengine.ext import ndb
import requests
from services import auth
import json

from HookEntity import HookEntity
from models import Account
from models import Product


class MenuUpdater:
    def addMenu(self, account_id):

        pass

    def updateMenu(self, entity):
        # type: (HookEntity) -> None
        product = ndb.get(account_id = entity.account, product_id = entity.object_id)
        if product is None:
            MenuUpdater.createMenuEntrie(entity)
        else:
            MenuUpdater.updateMenuEntrie(product, entity)

    @classmethod
    def updateMenuEntrie(cls, product, entity):
        token = auth.get_access_token(account_name=entity.account)
        r = requests.get(
            'https://{}.joinposter.com/api/menu.getProducts?token={}&product_id={}'.format(entity.account, token,
                                                                                           entity.object_id))
        data = json.loads(r)
        product(
            key=ndb.Key(Product, entity.product_id, parent=ndb.Key(Account, entity.account)),
            product_name=data['product_name'],
            product_id=data['product_id'],
            photo_origin=data['photo']
        ).put()

    @classmethod
    def createMenuEntrie(cls, entity):
        token = auth.get_access_token(account_name=entity.account)
        r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}&product_id={}'.format(entity.account, token, entity.object_id))
        data = json.loads(r)
        Product(
            key=ndb.Key(Product, entity.product_id, parent=ndb.Key(Account, entity.account)),
            product_name=data['product_name'],
            product_id = data['product_id'],
            photo_origin = data['photo']
        ).put()