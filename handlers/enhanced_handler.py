import webapp2
import jinja2
import os

from databases.secure_value import SecureValue

#create the paths for the templates
this_folder = os.path.dirname(__file__)
parent_folder = os.path.dirname(this_folder)
template_dir = os.path.join(parent_folder, 'templates')

#create the jinja environment
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class EnhancedHandler(webapp2.RequestHandler):
    """Extends the functionality of the webapp2.RequestHandler"""

    def __init__(self, *args, **kwargs):
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        self.arg_dict = {}
        self.SUPER_USERS = ['admin']
        self.user_name = self.read_secure_cookie('user_id')
        if self.user_name:
            self.arg_dict['user'] = self.user_name
        else:
            self.arg_dict['user'] = 'guest'

    def write(self, *args, **kwargs):
        """Shorthand for writing out
        Use it like self.response.out.write(*args, **kwargs)
        """
        self.response.out.write(*args, **kwargs)

    @staticmethod
    def render_str(template, **kwargs):
        t = jinja_env.get_template(template)
        return t.render(**kwargs)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

    def set_secure_cookie(self, cookie_name, value):
        cookie_value = SecureValue().make_secure_value(value)
        self.response.headers.add_header(
                        'Set-Cookie',
                        '%s=%s; Path=/' % (cookie_name, cookie_value))

    def read_secure_cookie(self, cookie_name):
        cookie_value = self.request.cookies.get(cookie_name)
        return cookie_value and SecureValue().check_secure_value(cookie_value)

    def login(self, user_key):
        self.set_secure_cookie('user_id', str(user_key))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def check_super_user(self, user_name):
        if user_name not in self.SUPER_USERS:
            self.render('sorry.html', **self.arg_dict)
            return False
        else:
            return True

    @staticmethod
    def convert_true_false(text_string):
        if text_string in ['t', 'T', 'True', 'true']:
            return True
        elif text_string in ['f', 'F', 'False', 'false']:
            return False
        else:
            return None

    def confirm_user_logged_in(self):
        if not self.user_name:
            self.redirect('/login')
            return False
        else:
            return True

    def bad_search(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('bad search')

    def add_page_name(self, page_name):
        self.arg_dict['page_name'] = page_name
