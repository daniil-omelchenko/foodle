from models import AccountModel
from services import products


def save_account(account_name, access_token):
    AccountModel(id=account_name, access_token=access_token).put()
    products.sync_products_for_account(account_name)


def get_access_token(account_name):
    account = AccountModel.get_by_id(account_name)
    if account:
        return account.access_token


def delete_account(account_name):
    AccountModel.get_by_id(account_name).key.delete()
    # todo: add call of products.remove_for_account(account_name)
