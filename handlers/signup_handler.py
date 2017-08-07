from enhanced_handler import EnhancedHandler
from databases.valid_inputs import ValidInputs
from databases.user import User
from databases.secure_value import SecureValue


class SignUpHandler(EnhancedHandler):
    """
    Handles the user signup page
    """
    def get(self):
        self.add_page_name('signup_page')
        print self.arg_dict
        self.render('signup_form.html', **self.arg_dict)

    def post(self):
        self.add_page_name('signup_page')
        #get the user inputs from the post request
        user_name = self.request.get('email_signup_name')
        password = self.request.get('password_signup_name')
        password_match = self.request.get('password_match_signup_name')
        phone_number = self.request.get('phone_number_signup_name')
        #email = self.request.get('email_signup_name')
        #roles = self.request.items()
        #roles = ['approver', 'saftey']


        self.arg_dict['user_name'] = user_name
        #self.arg_dict['email'] = email

        #Check to see that all of the inputs appear to be valid
        valid_inputs = ValidInputs()
        has_error = False
        # if not valid_inputs.valid_user_name(user_name):
        #     self.arg_dict['error_user_name'] = "That's not a valid username."
        #     has_error = True
        if not valid_inputs.valid_password(password):
            self.arg_dict['error_password'] = "That wasn't a valid password."
            has_error = True
        elif password != password_match:
            self.arg_dict['error_verify'] = "Your passwords didn't match."
            has_error = True
        if not valid_inputs.valid_email(user_name):
            self.arg_dict['error_email'] = "That's not a valid email."
            has_error = True
        if not valid_inputs.valid_phone_number(phone_number):
            self.arg_dict['error_phone_number'] = "That is not a valid phone number."
            has_error = True
        #if there was a bad value re-render the signup page
        if has_error:
            self.render('signup_form.html', **self.arg_dict)
        else:
            if User().by_user_name(user_name):
                self.arg_dict['error_email'] = "That user already exists."
                self.render('signup_form.html', **self.arg_dict)
                print 'r', self.arg_dict
            else:
                pw_hash = SecureValue().make_pw_hash(user_name, password)
                User().register_user(user_name, pw_hash, phone_number)
                self.login(user_name)  # fix this?
                self.redirect('/')
