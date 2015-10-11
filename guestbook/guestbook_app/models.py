from google.appengine.ext import ndb
from google.appengine.api import users

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_latest(cls,guestbook_name,count):
        try:
            return cls.query(ancestor = Guestbook.get_guestbook_key(guestbook_name)).order(-cls.date).fetch(count)
        except ValueError:
            return None

    @classmethod
    def put_from_dict(cls,dictionary):
        guestbook_name = dictionary.get("guestbook_name")
        if not guestbook_name :
            return DEFAULT_GUESTBOOK_NAME
        else:
            if Guestbook.is_exist(guestbook_name) is False:
                Guestbook.add_guestbook(guestbook_name)
            greeting = cls(parent = Guestbook.get_guestbook_key(guestbook_name))
            if users.get_current_user():
                greeting.author = users.get_current_user()
            greeting.content = dictionary.get("greeting_message")
            greeting.put()
            return guestbook_name


class Guestbook(ndb.Model):
    name = ndb.StringProperty(indexed=True)

    @staticmethod
    def get_guestbook(guestbook_name):
        try:
            return Guestbook.query(Guestbook.name == guestbook_name).get()
        except(RuntimeError,ValueError):
            return None


    @staticmethod
    def add_guestbook(guestbook_name):
        try:
            guestbook = Guestbook()
            guestbook.name = guestbook_name
            guestbook.put()
            return True
        except(RuntimeError,ValueError):
            return False

    @staticmethod
    def is_exist(guestbook_name):
        if Guestbook.get_guestbook(guestbook_name) is None:
            return False
        else:
            return True

    @staticmethod
    def get_guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
        return ndb.Key('Guestbook', guestbook_name)