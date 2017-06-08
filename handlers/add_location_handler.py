from handlers.enhanced_handler import EnhancedHandler
from shapes.polygon import Polygon
from converters.format_converter import FormatConverter
from databases.user import User
from managers.location_management import LocationManagement


class AddLocationHandler(EnhancedHandler):
    """
    Class handles the creation of a new location via a web request
    """
    def get(self):
        if not self.confirm_user_logged_in():
            return
        self.add_page_name('add_location')
        self.render('add_location_form.html', **self.arg_dict)

    def post(self):
        #get the variables from the post request
        descriptive_name = self.request.get('sight_name_location_name')
        points_string = self.request.get('points_string_name')
        #convert the points string to a list of point objects
        points_list = FormatConverter()\
            .convert_points_string_to_points_list(points_string)
        #create the polygon object
        polygon = Polygon()
        polygon.create_polygon_by_points(points_list)
        if not polygon.is_valid_polygon():
            #handle bad polygon here
            pass
        #get user object
        this_user = User().by_user_name(self.user_name)
        location_management = LocationManagement()
        #insert the location into the database
        pl_key = location_management.location_creation(this_user,
                                                       polygon,
                                                       descriptive_name)
        if pl_key:
            #if insert was successful redirect use to editing page
            url_safe_key = pl_key.urlsafe()
            self.redirect('/edit_location/' + url_safe_key)
        else:
            #if insert was unsuccessful handle it
            self.write('catch this error')