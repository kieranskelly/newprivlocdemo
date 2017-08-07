#import sys
#sys.path.insert(0, '/Users/kieran/google-cloud-sdk/platform/google_appengine/')
#sys.path.insert(0, '/Users/kieran/google-cloud-sdk/platform/google_appengine/lib/yaml/lib/')

from google.appengine.ext import ndb
from email import MIMEText

class User(ndb.Model):
    """
    Used to create a user entity and interact with the User database
    """
    user_name = ndb.StringProperty(required=True)   #user email = user_name
    pw_hash = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    roles = ndb.StringProperty(choices=['civilian', 'municipality', 'admin'], default='civilian')
    licenses = ''

    @staticmethod
    def phone_number_exists(phone_number):
        p = User.query(User.phone_number == phone_number)
        if p.count() > 0:
            return True
        else:
            return False

    # @staticmethod
    # def create_user(user_name, email, phone_number):
    #     user = User(user_name=user_name,
    #                 email=email,
    #                 phone_number=phone_number
    #                 )
    #     user_key = user.put()
    #     return user_key

    # returns the User, not the User key
    @staticmethod
    def by_phone_number(phone_number):
        pn = User.query(User.phone_number == phone_number)
        print 'pn', pn
        if pn.count() > 0:
            for p in pn:
                print 'p', p
                return p
        else:
            return False
    #
    # @staticmethod
    # def by_city(city):
    #     cit = User.query(User.city == city)
    #     if cit.count() > 0:
    #         for c in cit:
    #             return c
    #     else:
    #         return False

    ##############
    @staticmethod
    def by_id(user_id):
        return User.get_by_id(user_id)

    @staticmethod
    def by_user_name(user_name):
        user = User.query(User.user_name == user_name)
        if user.count() > 0:
            for u in user:
                return u
        else:
            return False

    @staticmethod
    def register_user(email, pw_hash, phone_number):
        user=User(user_name=email,
                        pw_hash=pw_hash,
                        phone_number=phone_number)

        user_key = user.put()
        return user_key

    def user_exists(self, user_name):
        user = self.by_user_name(user_name)
        if user:
            return True
        else:
            return False

