from handlers.enhanced_handler import EnhancedHandler
from databases.user import User
from databases.private_location import PrivateLocation


class ManageLocationsHandler(EnhancedHandler):
    """
    Handles displaying all of the users locations
    """
    def get(self):
        if not self.confirm_user_logged_in():
            return
        user = User().by_user_name(self.user_name)
        locations = PrivateLocation().get_all_locations_by_user(user)
        self.arg_dict['locations'] = {}
        for location in locations:
            self.location_to_arg_dict(location)
        self.add_page_name('manage_locations')
        self.render('manage_locations_form.html', **self.arg_dict)

    def location_to_arg_dict(self, location):
        key = location.key.urlsafe()
        self.arg_dict['locations'][key] = {}
        self.arg_dict['locations'][key]['descriptive_name'] = location.descriptive_name
        self.arg_dict['locations'][key]['max_latitude'] = location.max_latitude
        self.arg_dict['locations'][key]['min_latitude'] = location.min_latitude
        self.arg_dict['locations'][key]['max_longitude'] = location.max_longitude
        self.arg_dict['locations'][key]['min_longitude'] = location.min_longitude