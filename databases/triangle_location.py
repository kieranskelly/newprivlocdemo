from google.appengine.ext import ndb


class TriangleLocation(ndb.Model):
    """
    This class handles creating and editing triangles database objects
    """
    private_location_fk = ndb.KeyProperty(kind='PrivateLocation')
    max_latitude = ndb.FloatProperty()
    min_latitude = ndb.FloatProperty()
    max_longitude = ndb.FloatProperty()
    min_longitude = ndb.FloatProperty()
    point_a = ndb.GeoPtProperty()
    point_b = ndb.GeoPtProperty()
    point_c = ndb.GeoPtProperty()
    triangle = ndb.PickleProperty()

    @staticmethod
    def create_location(pl_key,
                        triangle):
        """
        Creates a triangle database object.
        :param pl_key: key object of the parent location
        :param triangle: Triangle object
        :return: key of the database  object
        """
        triangle_location = TriangleLocation(
            private_location_fk=pl_key,
            max_latitude=triangle.get_max_lat(),
            min_latitude=triangle.get_min_lat(),
            max_longitude=triangle.get_max_lng(),
            min_longitude=triangle.get_min_lng(),
            point_a=ndb.GeoPt(triangle.point_a.get_lat(),
                              triangle.point_a.get_lng()),
            point_b=ndb.GeoPt(triangle.point_b.get_lat(),
                              triangle.point_b.get_lng()),
            point_c=ndb.GeoPt(triangle.point_c.get_lat(),
                              triangle.point_c.get_lng()),
            triangle=triangle
        )
        return triangle_location.put()

    @staticmethod
    def get_triangles_for_private_location(pl_key):
        """
        Get all of the children triangle for a given location
        :param pl_key: foreign key object of location
        :return: Iterable
        """
        return TriangleLocation()\
            .query(TriangleLocation.private_location_fk == pl_key)

    def remove_triangles_for_private_location(self, pl_key):
        """
        Remove triangle objects from the database for a given location
        :param pl_key: foreign key object of location
        :return: None
        """
        to_remove = self.get_triangles_for_private_location(pl_key)
        for location in to_remove:
            location.key.delete()

    def convert_triangle_to_dictionary(self):
        """
        Converts a database object to a dictionary
        :return: Dictionary
        """
        triangle = dict()
        triangle['max_latitude'] = self.max_latitude
        triangle['min_latitude'] = self.min_latitude
        triangle['max_longitude'] = self.max_longitude
        triangle['min_longitude'] = self.min_longitude
        triangle['point_a_latitude'] = self.triangle.point_a.get_lat()
        triangle['point_a_longitude'] = self.triangle.point_a.get_lng()
        triangle['point_b_latitude'] = self.triangle.point_b.get_lat()
        triangle['point_b_longitude'] = self.triangle.point_b.get_lng()
        triangle['point_c_latitude'] = self.triangle.point_c.get_lat()
        triangle['point_c_longitude'] = self.triangle.point_c.get_lng()
        return triangle