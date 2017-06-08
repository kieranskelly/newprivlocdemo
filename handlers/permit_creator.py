from handlers.edit_location_handler import EnhancedHandler


class CreatePermit(EnhancedHandler):

    def get(self):
        if not self.confirm_user_logged_in():
            return
        self.add_page_name('permit_maker')
        self.render('permit_maker.html', **self.arg_dict)