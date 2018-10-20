from models import AccountModel
from services import products, company_settings


def save_account(account_name, access_token):
    settings = company_settings.get_company_settings(account_name, access_token)
    AccountModel(
        id=account_name,
        access_token=access_token,
        company_name=settings.company_name,
        currency=settings.currency,
        logo_url=settings.logo_url,
        address=settings.address,
        phone=settings.phone
    ).put()
    products.sync_products_for_account(account_name, access_token)


def get_access_token(account_name):
    account = AccountModel.get_by_id(account_name)
    if account:
        return account.access_token


def delete_account(account_name):
    account = AccountModel.get_by_id(account_name)
    if account:
        account.key.delete()
    # todo: add call of products.remove_for_account(account_name)
