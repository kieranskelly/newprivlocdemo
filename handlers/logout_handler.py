from handlers.enhanced_handler import EnhancedHandler


class LogoutHandler(EnhancedHandler):
    """
    Handled a logout request
    """

    def get(self):
        """
        logs user out of session
        :return:
        """
        self.logout()
        self.redirect('/')
