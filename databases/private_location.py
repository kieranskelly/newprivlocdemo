from google.appengine.ext import ndb
from devices.camera import Camera
from devices.video import Video
from statuses.location_status import LocationStatus


class PrivateLocation(ndb.Model):
    """This class creates a ndb object for describing a private location."""
    user_fk = ndb.KeyProperty(kind='User')
    descriptive_name = ndb.StringProperty()
    max_latitude = ndb.FloatProperty()
    min_latitude = ndb.FloatProperty()
    max_longitude = ndb.FloatProperty()
    min_longitude = ndb.FloatProperty()
    center = ndb.GeoPtProperty()
    polygon = ndb.PickleProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    camera = ndb.PickleProperty()
    video = ndb.PickleProperty()
    status = ndb.PickleProperty()
    zip_code = ndb.StringProperty()

    @staticmethod
    def create_location(user, polygon, descriptive_name, zip_code):
        """Takes as input a polygon object and a string naming the location.
        Returns the key of the newly created database object.
        """
        private_location = PrivateLocation(user_fk=user.key,
                                           descriptive_name=descriptive_name,
                                           max_latitude=polygon.get_max_lat(),
                                           min_latitude=polygon.get_min_lat(),
                                           max_longitude=polygon.get_max_lng(),
                                           min_longitude=polygon.get_min_lng(),
                                           center=ndb.GeoPt(polygon.get_center_lat(),
                                                            polygon.get_center_lng()),
                                           polygon=polygon,
                                           camera=Camera(),
                                           video=Video(),
                                           status=LocationStatus(),
                                           zip_code=zip_code
                                           )
        return private_location.put()

    @staticmethod
    def get_location_by_key(pl_key):
        return PrivateLocation().get_by_id(pl_key.id())

    @staticmethod
    def get_location_by_id(private_location_id):
        return PrivateLocation().get_by_id(private_location_id)

    def check_user_access(self, pl_key, user):
        """Takes as an argument a private location key and a user object.
        Returns a boolean of whether or not the user is the owner of a
        location.
        """
        return self.get_location_by_key(pl_key).user_fk == user.key

    @staticmethod
    def get_all_locations_by_user(user):
        """Takes as input a user object and returns all locations owned
        by that user.
        """
        return PrivateLocation.query(PrivateLocation.user_fk == user.key)

    @staticmethod
    def get_all_locations_by_zip(zip_code):
        """Takes as input a user object and returns all locations owned
        by that user.
        """
        return PrivateLocation.query(PrivateLocation.zip_code == zip_code)

    @staticmethod
    def delete_location(pl_key):
        pl_key.delete()

    @staticmethod
    def get_locations_within_box(lat, lng, lat_inc, lng_inc):
        """takes as input a latitude and a longitude as well as the lat and lng
        increment steps for the box to be built around the point.  Returns all
        locations whose centers are within the described box
        """

        results = PrivateLocation.query(PrivateLocation.min_latitude <= lat+lat_inc)
        locations = list()
        for r in results:
            if r.max_latitude >= lat - lat_inc and\
                r.max_longitude >= lng - lng_inc and\
                r.min_longitude <= lng + lng_inc:
                locations.append(r)
        return locations

    def convert_location_to_dictionary(self):
        """Helper function to convert a location to a dictionary."""
        location = dict()
        location['key'] = self.key.id()
        location['descriptive_name'] = self.descriptive_name
        location['max_latitude'] = self.max_latitude
        location['min_latitude'] = self.min_latitude
        location['center_latitude'] = (self.max_latitude + self.min_latitude)/2.
        location['max_longitude'] = self.max_longitude
        location['min_longitude'] = self.min_longitude
        location['center_longitude'] = (self.max_longitude + self.min_longitude)/2.
        location['location_active'] = self.status.active
        location['camera_active'] = self.camera.active
        location['camera_message'] = self.camera.message_text
        location['video_active'] = self.video.active
        location['video_message'] = self.video.message_text
        location['zip_code'] = self.zip_code
        return location