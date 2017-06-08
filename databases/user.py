from google.appengine.ext import ndb


class User(ndb.Model):
    """
    Used to create a user entity and interact with the User database
    """
    user_name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

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
    def register_user(user_name, pw_hash, email):
        user = User(user_name=user_name,
                    pw_hash=pw_hash,
                    email=email)
        user_key = user.put()
        return user_key

    def user_exists(self, user_name):
        user = self.by_user_name(user_name)
        if user:
            return True
        else:
            return False
