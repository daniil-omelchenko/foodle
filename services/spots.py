from google.appengine.ext import ndb

import requests
from domain.product import Product
from domain.spot import Spot

from services import account

from models import ProductModel, AccountModel, SpotModel, SpotProductModel


def save_spot(spot, product_id, price):
    # type: (Spot, str) -> None
    SpotModel(
        spot_id=spot.spot_id,
        spot_name=spot.spot_name,
        spot_address=spot.spot_address,
    ).put()
    SpotProductModel(
        spot_id=spot.spot_id,
        product_id=product_id,
        price=price
    ).put()

def sync_spot(spot, account, product_id):
    r = get_spot_for_product(spot, account)
    save_spot(r, product_id, spot['price'])

def get_spot_for_product(spot_from_product, account):
    # type: (str, str) -> Spot
    token = account.get_access_token(account)
    r = requests.get(
        'https://{}.joinposter.com/api/menu.getSpots?token={}'.format(account, token))
    spot_list = r.json().get('response')
    for spot in spot_list:
        spot_obj = Spot.deserialize(spot)
        if spot_obj.spot_id == spot_from_product['spot_id']:
            return spot_obj
    return None