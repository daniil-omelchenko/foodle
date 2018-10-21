from google.appengine.ext import ndb
from geopy.geocoders import GoogleV3
import requests
from domain.hook_update import HookUpdate, HookAction
from domain.spot import Spot

from models import AccountModel, SpotModel, SpotProductModel
from services.settings import settings


geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)


def save_spot(spot, account_id, product_id=None, price=None):
    # type: (Spot, str, account_id, str) -> None

    lat, lon = None, None
    location = geolocator.geocode(spot.spot_address)
    if location:
        lat, lon = location.latitude, location.longitude

    SpotModel(
        key=ndb.Key(SpotModel, spot.spot_id, parent=ndb.Key(AccountModel, account_id)),
        spot_id=spot.spot_id,
        spot_name=spot.spot_name,
        spot_address=spot.spot_address,
        lat=lat,
        lon=lon
    ).put()
    if price:
        SpotProductModel(
            id='{}:{}'.format(spot.spot_id, product_id),
            spot_id=spot.spot_id,
            product_id=product_id,
            price=price
        ).put()
    else:
        SpotProductModel(
            spot_id=spot.spot_id,
            product_id=product_id
        ).put()


def sync_spot(spot, account_id, product_id, token):
    r = get_spot_for_product(spot["spot_id"], account_id, token)
    save_spot(r, account_id, product_id, spot['price'])


def get_spot_for_product(spot_from_product, account_id, token):
    # type: (str, str) -> Spot
    r = requests.get(
        'https://{}.joinposter.com/api/access.getSpots?token={}'.format(account_id, token))
    spot_list = map(Spot.deserialize, r.json().get('response'))
    for spot in spot_list:
        if spot.spot_id == spot_from_product:
            return spot


# ToDo: complete
def remove_spot(object_id, account):
    pass


def update_by_hook(hook_update, token):
    # type: (HookUpdate, str) -> None
    if hook_update.action == HookAction.CHANGED:
        spot = get_spot_for_product(hook_update.object_id, hook_update.account, token)
        save_spot(spot, hook_update.account)
    elif hook_update.action == HookAction.ADDED:
        spot = get_spot_for_product(hook_update.object_id, hook_update.account, token)
        save_spot(spot, hook_update.account)
    elif hook_update.action == HookAction.REMOVED:
        remove_spot(hook_update.object_id, hook_update.account)
