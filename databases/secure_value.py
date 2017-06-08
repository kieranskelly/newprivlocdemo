import random
import hashlib
import hmac
from string import letters
import secret


class SecureValue:
    """
    Class handles creating and read secure values.
    """

    def __init__(self):
        self.secret = secret.SECRET

    def make_secure_value(self, value):
        """
        Creates a string that can be used to confirm a users identity
        :param value: String
        :return: String of a value and its hmaced value separated by a '|'
        """
        return '%s|%s' % (value, hmac.new(self.secret, value).hexdigest())

    def check_secure_value(self, secure_value):
        """
        Reads a secure values and checks to see if it a valid value.
        :param secure_value: String
        :return: Boolean
        """
        value = secure_value.split('|')[0]
        if secure_value == self.make_secure_value(value):
            return value
        else:
            return False

    @staticmethod
    def _make_salt(length=5):
        """
        Create a string of random letters and numbers of given length
        :param length: int
        :return: String
        """
        return ''.join(random.choice(letters) for _ in range(length))

    def make_pw_hash(self, user_name, password, salt=None):
        """
        Creates a hashed password string
        :param user_name: String
        :param password: String
        :param salt: String
        :return: String of the salt and hashed password separated by '|'
        """
        if not salt:
            salt = self._make_salt()
        pw_hash = hashlib.sha256(user_name+password+salt).hexdigest()
        return '%s|%s' % (salt, pw_hash)

    def check_valid_password(self, user_name, password, pw_hash):
        """
        Check to see if a username, password and password hash are valid
        :param user_name: String
        :param password: String
        :param pw_hash: String
        :return: Boolean
        """
        salt = pw_hash.split('|')[0]
        return pw_hash == self.make_pw_hash(user_name, password, salt)
