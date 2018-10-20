from google.appengine.ext import ndb


SUPPORT = ['mashsheva', 'Danik_O']
ADMINS = ['elijah_om', 'Danik_O', 'mashsheva']


class UserState(object):
    INIT = 'INIT'
    BROADCASTING = 'BROADCASTING'
    ASKING_A_QUESTION = 'ASKING_A_QUESTION'


class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    type = ndb.StringProperty()
    state = ndb.StringProperty(default=UserState.INIT, indexed=True)

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


class ProductModel(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'Product'

    product_name = ndb.StringProperty(indexed=True)
    product_id = ndb.StringProperty(indexed=True)
    photo_origin = ndb.StringProperty()
