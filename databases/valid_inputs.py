import re


class ValidInputs:
    """
    Class validates input before it is to be processed
    """

    @staticmethod
    def valid_user_name(user_name):
        """
        Checks to see if the username is valid
        :param user_name: String
        :return: Boolean
        """
        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return user_name and user_re.match(user_name)

    @staticmethod
    def valid_password(password):
        """
        Checks to see if a password is valid
        :param password: String
        :return: Boolean
        """
        pass_re = re.compile(r"^.{3,20}$")
        return password and pass_re.match(password)

    @staticmethod
    def valid_email(email):
        """
        Checks to see if a email address appears valid
        :param email: String
        :return: Boolean
        """
        email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return email and email_re.match(email)

    @staticmethod
    def valid_phone_number(phone_number):
        if len(phone_number) != 10:
            return False
        for i in range(10):
            # if i in [3,7]:
            #     if phone_number[i] != '-':
            #         return False
            if not phone_number[i].isalnum():
                return False
        return True

    @staticmethod
    def check_user_lat_long_inputs(current_form):
        """
        Checks to see if latitude and longitude are within valid region.
        Currently unused and most likely unneeded
        :param current_form: web form
        :return: Booolean
        """
        #refactor from here
        try:
            current_form.max_latitude = float(current_form.max_latitude)
        except:
            current_form.arg_dict['error_max_latitude'] = 'Latitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        try:
            current_form.min_latitude = float(current_form.min_latitude)
        except:
            current_form.arg_dict['error_min_latitude'] = 'Latitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        try:
            current_form.max_longitude = float(current_form.max_longitude)
        except:
            current_form.arg_dict['error_max_longitude'] = 'Longitude must be a number between -180 and 180 inclusive.'
            current_form.has_error = True

        try:
            current_form.min_longitude = float(current_form.min_longitude)
        except:
            current_form.arg_dict['error_min_longitude'] = 'Longitude must be a number between -180 and 180 inclusive.'
            current_form.has_error = True

        if -90 > current_form.max_latitude or current_form.max_latitude > 90:
            current_form.arg_dict['error_max_latitude'] = 'Latitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        if -90 > current_form.min_latitude or current_form.min_latitude > 90:
            current_form.arg_dict['error_min_latitude'] = 'Latitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        if -180 > current_form.max_longitude or current_form.max_longitude > 180:
            current_form.arg_dict['error_max_longitude'] = 'Longitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        if -180 > current_form.min_longitude or current_form.min_longitude > 180:
            current_form.arg_dict['error_min_longitude'] = 'Longitude must be a number between -90 and 90 inclusive.'
            current_form.has_error = True

        if current_form.max_latitude <= current_form.min_latitude:
            current_form.arg_dict['error_max_latitude'] = 'Max Latitude must be greater than Min Latitude'
            current_form.has_error = True

        if current_form.max_longitude <= current_form.min_longitude:
            current_form.arg_dict['error_max_longitude'] = 'Max Longitude must be greater than Min Longitude'
            current_form.has_error = True
        #to here
        return current_form