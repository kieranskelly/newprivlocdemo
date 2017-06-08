import urllib
from google.appengine.ext import ndb
from handlers.enhanced_handler import EnhancedHandler
from databases.user import User
from databases.private_location import PrivateLocation
from databases.triangle_location import TriangleLocation
from managers.location_management import LocationManagement
from shapes.polygon import Polygon
from converters.format_converter import FormatConverter


class JustTheMapHandler(EnhancedHandler):
    """
    Class handle the editing of a location via web requests
    """
    def get(self):
        """
        Render the requested location for editing
        :param resource: url safe location key
        :return:
        """
        try:
            location_id = int(self.request.get('locationID'))
            location_key = ndb.Key('PrivateLocation', location_id)
            self.resource_string = location_id
            self.location = PrivateLocation().get_location_by_key(location_key)
        except:
            self.write('error getting the key')
            return

        #create dictionary that will hold all the variables for the location
        self.arg_dict['location'] = {}
        self.add_location_to_arg_dict()
        self.get_points_from_db_and_convert_to_array()
        #self.write(self.arg_dict)
        self.render('just_the_map2.html', **self.arg_dict)

    def add_location_to_arg_dict(self):
        """
        helper function to create a dictionary for use by the template
        :return:
        """
        self.arg_dict['location']['key'] = self.resource_string
        self.arg_dict['location']['descriptive_name'] = self.location.descriptive_name
        self.arg_dict['location']['max_latitude'] = self.location.max_latitude
        self.arg_dict['location']['min_latitude'] = self.location.min_latitude
        self.arg_dict['location']['max_longitude'] = self.location.max_longitude
        self.arg_dict['location']['min_longitude'] = self.location.min_longitude
        self.arg_dict['location']['active'] = self.location.status.active
        self.arg_dict['location']['validated'] = self.location.status.validated
        self.arg_dict['location']['camera'] = self.location.camera.active
        self.arg_dict['location']['camera_text'] = self.location.camera.message_text
        self.arg_dict['location']['video'] = self.location.video.active
        self.arg_dict['location']['video_text'] = self.location.video.message_text
        self.arg_dict['location']['zip_code'] = self.location.zip_code

    def get_points_from_db_and_convert_to_array(self):
        """
        converts list of points to a points string
        :return:
        """
        '''Probably should be moved to the format converter'''
        points_list = []
        for point in self.location.polygon.polygon_points:
            lat = point.get_lat()
            lng = point.get_lng()
            points_list.append([lat,lng])
        self.arg_dict['location']['points'] = points_list
        triangle_list = []
        triangle_location = TriangleLocation()
        triangles = triangle_location.get_triangles_for_private_location(self.location.key)
        for triangle in triangles:
            triangle_list.append([[triangle.point_a.lat,
                                   triangle.point_a.lon],
                                  [triangle.point_b.lat,
                                   triangle.point_b.lon],
                                   [triangle.point_c.lat,
                                   triangle.point_c.lon]])
        self.arg_dict['location']['triangles'] = triangle_list


class EditLocationHandler(EnhancedHandler):
    """
    Class handle the editing of a location via web requests
    """
    def get(self, resource):
        """
        Render the requested location for editing
        :param resource: url safe location key
        :return:
        """
        #confirm user logged in
        if not self.confirm_user_logged_in():
            return
        self.get_resources(resource)
        private_location = PrivateLocation()
        #confirm user owns location
        if not private_location.check_user_access(self.location.key,
                                                  self.user):
            self.write('User does not have access')
            return
        #create dictionary that will hold all the variables for the location
        self.arg_dict['location'] = {}
        self.add_location_to_arg_dict()
        self.get_points_from_db_and_convert_to_array()
        self.render('edit_location_form.html', **self.arg_dict)

    def post(self, resource):
        """
        Handles an edited location
        :param resource: url safe location key
        :return:
        """
        self.get_resources(resource)

        if self.request.get('delete_location'):
            LocationManagement().delete_location(self.location.key)
            self.redirect('/manage_locations')

        elif self.request.get('save_location'):
            #get the variables from the post request
            descriptive_name = self.request.get('descriptive_name')
            active = self.request.get('active')
            camera = self.request.get('camera')
            camera_text = self.request.get('camera_text')
            video = self.request.get('video')
            video_text = self.request.get('video_text')
            points_string = self.request.get('points_string_name')
            zip_code = self.request.get('zip_code')
            #convert the points string to a list of points
            points_list = FormatConverter()\
                .convert_points_string_to_points_list(points_string)

            #create new polygon
            new_polygon = Polygon()
            new_polygon.create_polygon_by_points(points_list)

            #check to see if the polygon is valid
            if not new_polygon.is_valid_polygon():
                #if not valid redirect to unedited version of location
                url_safe_key = self.location.key.urlsafe()
                self.redirect('/edit_location/' + url_safe_key)
                return
            #check to see if the polygon has changed
            polygons_match = new_polygon\
                .polygon_is_equivalent(self.location.polygon)
            if not polygons_match:
                '''if the polygon was edited remove all old children and
                inserts new children for the location'''
                self.location.polygon = new_polygon
                LocationManagement()\
                    .edit_location_with_polygon_change(new_polygon,
                                                       self.location.key)
            #set fields of db object and put it to the db
            self.location.descriptive_name = descriptive_name
            self.location.status.active = self.convert_true_false(active)
            self.location.camera.active = self.convert_true_false(camera)
            self.location.camera.message_text = camera_text
            self.location.video.active = self.convert_true_false(video)
            self.location.video.message_text = video_text
            self.location.zip_code = zip_code
            self.location.put()

            #redirect to the location edit page
            self.url_safe_key = self.location.key.urlsafe()
            self.redirect('/edit_location/' + self.url_safe_key)

    def get_resources(self, resource):
        """
        helper function to get the variable from the request
        :param resource: http request document
        :return:
        """
        self.resource = resource
        self.resource_string = urllib.unquote(resource)
        self.resource_key = ndb.Key(urlsafe=self.resource_string)
        self.location = self.resource_key.get()
        self.user = User().by_user_name(self.user_name)

    def add_location_to_arg_dict(self):
        """
        helper function to create a dictionary for use by the template
        :return:
        """
        self.arg_dict['location']['key'] = self.resource_string
        self.arg_dict['location']['descriptive_name'] = self.location.descriptive_name
        self.arg_dict['location']['max_latitude'] = self.location.max_latitude
        self.arg_dict['location']['min_latitude'] = self.location.min_latitude
        self.arg_dict['location']['max_longitude'] = self.location.max_longitude
        self.arg_dict['location']['min_longitude'] = self.location.min_longitude
        self.arg_dict['location']['active'] = self.location.status.active
        self.arg_dict['location']['validated'] = self.location.status.validated
        self.arg_dict['location']['camera'] = self.location.camera.active
        self.arg_dict['location']['camera_text'] = self.location.camera.message_text
        self.arg_dict['location']['video'] = self.location.video.active
        self.arg_dict['location']['video_text'] = self.location.video.message_text
        self.arg_dict['location']['zip_code'] = self.location.zip_code

    def get_points_from_db_and_convert_to_array(self):
        """
        converts list of points to a points string
        :return:
        """
        '''Probably should be moved to the format converter'''
        points_list = []
        for point in self.location.polygon.polygon_points:
            lat = point.get_lat()
            lng = point.get_lng()
            points_list.append([lat,lng])
        self.arg_dict['location']['points'] = points_list
        triangle_list = []
        triangle_location = TriangleLocation()
        triangles = triangle_location.get_triangles_for_private_location(self.location.key)
        for triangle in triangles:
            triangle_list.append([[triangle.point_a.lat,
                                   triangle.point_a.lon],
                                  [triangle.point_b.lat,
                                   triangle.point_b.lon],
                                   [triangle.point_c.lat,
                                   triangle.point_c.lon]])
        self.arg_dict['location']['triangles'] = triangle_list