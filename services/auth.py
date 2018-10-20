from models import Account


def save_account(account_name, access_token):
    Account(id=account_name, access_token=access_token).put()


def get_access_token(account_name):
    account = Account.get_by_id(account_name)
    if account:
        return account.access_token
