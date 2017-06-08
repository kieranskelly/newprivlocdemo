from handlers.enhanced_handler import EnhancedHandler
from databases.user import User
from databases.secure_value import SecureValue


class LoginHandler(EnhancedHandler):
    """
    Handles logging in a user
    """

    def get(self):
        self.add_page_name('login_page')
        self.render('login_form.html', **self.arg_dict)

    def post(self):
        self.add_page_name('login_page')
        user_name = self.request.get('user_name_login_name')
        password = self.request.get('password_login_name')

        has_error = False
        #check to see if the username is in the User db
        user = User().by_user_name(user_name)
        if not user:
            self.arg_dict['error_msg'] = "Invalid user name."
            has_error = True
        else:
            #check to see if usename and password are valid
            secure = SecureValue().check_valid_password(user_name,
                                                        password,
                                                        user.pw_hash)
            if not secure:
                self.arg_dict['error_msg'] = "Password not valid for user."
                has_error = True

        if has_error:
            self.render('login_form.html', **self.arg_dict)
        else:
            self.login(user.user_name)
            self.redirect('/')