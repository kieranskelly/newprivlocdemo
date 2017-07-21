from handlers.edit_location_handler import EnhancedHandler

class PreFlight(EnhancedHandler):
    def get(self):
        self.render('preflight.html')

    def post(self):
        pass