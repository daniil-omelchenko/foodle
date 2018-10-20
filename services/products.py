import requests
from services import auth
from models import Product


def sync_products_for_account(account):
    token = auth.get_access_token(account)
    r = requests.get('https://{}.joinposter.com/api/menu.getProducts?token={}'.format(account, token))


def save_product():
    Product(

    )
