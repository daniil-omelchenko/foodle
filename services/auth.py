from models import Account
from services import products


def save_account(account_name, access_token):
    Account(id=account_name, access_token=access_token).put()
    products_array = products.sync_products_for_account()


def get_access_token(account_name):
    account = Account.get_by_id(account_name)
    if account:
        return account.access_token
