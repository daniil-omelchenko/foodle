from google.appengine.ext import ndb

from HookEntity import HookEntity
from models import Account


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

        pass

    @classmethod
    def createMenuEntrie(cls, entity):
        pass