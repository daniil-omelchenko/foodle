from google.appengine.ext import ndb


SUPPORT = ['mashsheva', 'Danik_O']
ADMINS = ['elijah_om', 'Danik_O', 'mashsheva']


class UserState(object):
    INIT = 'INIT'
    BROADCASTING = 'BROADCASTING'
    ASKING_A_QUESTION = 'ASKING_A_QUESTION'


class QuestionState(object):
    ASKED = 'ASKED'
    ANSWERED = 'ANSWERED'


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


class Question(ndb.Model):
    user_key = ndb.KeyProperty(kind=User)
    question = ndb.StringProperty()
    state = ndb.StringProperty(indexed=True)
    answer = ndb.StringProperty()


class Schedule(ndb.Model):
    datetime = ndb.DateTimeProperty()
    event = ndb.StringProperty()
    comment = ndb.StringProperty()

