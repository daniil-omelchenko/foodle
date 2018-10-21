from google.appengine.ext import ndb


SUPPORT = ['mashsheva', 'Danik_O']
ADMINS = ['elijah_om', 'Danik_O', 'mashsheva']


class UserState(object):
    INIT = 'INIT'
    BROADCASTING = 'BROADCASTING'
    ASKING_A_QUESTION = 'ASKING_A_QUESTION'


class User(ndb.Expando):
    username = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    type = ndb.StringProperty()
    state = ndb.StringProperty(default=UserState.INIT, indexed=True)
    lon = ndb.StringProperty()
    lat = ndb.StringProperty()
    location_updated = ndb.DateTimeProperty()

    @property
    def is_admin(self):
        return self.username in ADMINS

    def set_state(self, state):
        self.state = state
        self.put()

    @classmethod
    def get_by_username(cls, username):
        users = cls.query(cls.username == username).fetch(limit=1)
        return users[0] if users else None


class AccountModel(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'Account'

    access_token = ndb.StringProperty()
    company_name = ndb.StringProperty()
    currency = ndb.StringProperty()
    logo_url = ndb.StringProperty()
    address = ndb.StringProperty()
    phone = ndb.StringProperty()


class ProductModel(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'Product'

    product_name = ndb.StringProperty(indexed=True)
    product_id = ndb.StringProperty(indexed=True)
    photo_url = ndb.StringProperty()
    category_name = ndb.StringProperty()


class SpotModel(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'Spot'

    spot_id = ndb.StringProperty(indexed=True)
    spot_name = ndb.StringProperty(indexed=True)
    spot_adress = ndb.StringProperty()
    spot_lon = ndb.StringProperty()
    spot_lat = ndb.StringProperty()


class SpotProductModel(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'SpotProduct'

    spot_id = ndb.StringProperty(indexed=True)
    product_id = ndb.StringProperty(indexed=True)
    price = ndb.StringProperty()
