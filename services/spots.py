from google.appengine.ext import ndb
from geopy.geocoders import Nominatim
import requests
from domain.product import Product
from domain.spot import Spot

from services import account

from models import ProductModel, AccountModel, SpotModel, SpotProductModel


def save_spot(spot, product_id, price):
    # type: (Spot, str) -> None
    lat=None
    lon=None
    try:
        geolocator = Nominatim(user_agent="foodle")#what for user_agent
        location = geolocator.geocode(spot.spot_address)
        lat, lon = location.latitude, location.longitude
    except Exception:
        pass

    SpotModel(
        spot_id=spot.spot_id,
        spot_name=spot.spot_name,
        spot_address=spot.spot_address,
        lat=lat,
        lon=lon
    ).put()
    SpotProductModel(
        spot_id=spot.spot_id,
        product_id=product_id,
        price=price
    ).put()

def sync_spot(spot, account_id, product_id):
    r = get_spot_for_product(spot, account_id)
    save_spot(r, product_id, spot['price'])

def get_spot_for_product(spot_from_product, account_id):
    # type: (str, str) -> Spot
    token = account.get_access_token(account_id)
    r = requests.get(
        'https://{}.joinposter.com/api/menu.getSpots?token={}'.format(account_id, token))
    spot_list = r.json().get('response')
    for spot in spot_list:
        spot_obj = Spot.deserialize(spot)
        if spot_obj.spot_id == spot_from_product['spot_id']:
            return spot_obj
    return None