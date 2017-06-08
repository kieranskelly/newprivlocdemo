from enhanced_handler import EnhancedHandler


class LandingPageHandler(EnhancedHandler):
    """Handles requests for the main landing page"""

    def get(self):
        self.render('landing_page_form.html', **self.arg_dict)