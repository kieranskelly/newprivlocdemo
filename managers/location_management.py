from databases.private_location import PrivateLocation
from databases.triangle_location import TriangleLocation
from databases.private_location_index import PrivateLocationIndex
from google.appengine.api import urlfetch
import json


class LocationManagement:
    """
    Class handles location creation and editing.  Communicates with the
    TriangleLocation DB, PrivateLocation DB and the PrivateLocationIndex.
    """

    @staticmethod
    def location_creation(user, polygon, descriptive_name):
        """
        Handles all the aspects of adding a new location
        :param user: User DB object
        :param polygon: Polygon object
        :param descriptive_name: String name of location
        :return: return the key if the new PrivateLocation object
        """
        zip_code = ""
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
            url += str(polygon.get_center_lat()) + "," + str(polygon.get_center_lng())
            url += "&key=AIzaSyBYZ4U65PtFBrIpAimLtporw8ehdvXBo6k"
            response = urlfetch.fetch(url)
            if response.status_code == 200:
                data = json.loads(response.content)
                zip_code = data['results'][0]['address_components'][-2]['long_name']
        except:
            pass

        triangles = polygon.polygon_triangulation()
        #insert location in DB
        private_location = PrivateLocation()
        pl_key = private_location.create_location(user,
                                                  polygon,
                                                  descriptive_name,
                                                  zip_code)
        #insert all of the triangles to the DB
        for triangle in triangles:
            triangle_location = TriangleLocation()
            tl_key = triangle_location.create_location(pl_key,
                                                       triangle)
        #add location to the search index
        pli = PrivateLocationIndex()
        pli.create_location(polygon.get_center_lat(),
                            polygon.get_center_lng(),
                            pl_key
                            )

        return pl_key

    @staticmethod
    def delete_location(pl_key):
        """
        removes location triangle and index
        :param pl_key: Key of PrivateLocation
        :return:
        """
        PrivateLocation().delete_location(pl_key)
        PrivateLocationIndex().delete_location(pl_key)
        TriangleLocation().remove_triangles_for_private_location(pl_key)

    @staticmethod
    def get_locations_within_radius_complex(lat, lng, radius_in_miles=5):
        """
        uses the Search API index to get locations in the area
        :param lat: float
        :param lng: float
        :param radius_in_miles: float *optional
        :return: iterable
        """
        pli = PrivateLocationIndex()
        index_result = pli.get_locations_within_radius(radius_in_miles,
                                                       lat,
                                                       lng)
        locations = []
        for result in index_result:
            this_id = int(result.fields[1].value)
            private_location = PrivateLocation().get_location_by_id(this_id)
            locations.append(private_location)
        return locations

    @staticmethod
    def get_locations_within_radius_simple(lat, lng, radius_in_miles=5):
        pass

    @staticmethod
    def get_triangles_for_location(private_location):
        """
        Helper function to get all children TriangleLocations for a
        PrivateLocation
        :param private_location: Key of PrivateLocation
        :return: Iterable
        """
        tl = TriangleLocation()
        triangles = tl.get_triangles_for_private_location(private_location.key)
        triangle_list = list()
        #new line start
        if triangles:
        #end new line
        #new indent start
            for triangle in triangles:
                triangle_list.append(triangle)
        #end new indent start
        return triangle_list

    @staticmethod
    def convert_locations_and_triangles_to_json(locations=None, triangles=None):
        """
        Helper function to convert PrivateLocations and TriangleLocations
        to a json document.
        :param locations: List of PrivateLocation objects
        :param triangles: List of TriangleLocation objects
        :return: JSON document
        """
        results = dict()
        if locations:
            results['locations'] = dict()
            for location in locations:
                results['locations'][location.key.id()] = location\
                    .convert_location_to_dictionary()
        if triangles:
            results['triangles'] = dict()
            for triangle in triangles:
                if not triangle.private_location_fk.id() in results['triangles']:
                    results['triangles'][triangle.private_location_fk.id()] = dict()
                results['triangles']\
                    [triangle.private_location_fk.id()]\
                    [triangle.key.id()] = triangle.convert_triangle_to_dictionary()
        return json.dumps(results)

    def get_locations_within_radius_complex_json(self, lat, lng,
                                                 radius_in_miles=5):
        """
        Gets all of the locations within the circle described by the point
        and radius of the circle.  Uses a Complex API search.
        Fast but expensive
        :param lat: float
        :param lng: float
        :param radius_in_miles: float *optional
        :return: Iterable
        """
        locations = self.get_locations_within_radius_complex(lat,
                                                             lng,
                                                             radius_in_miles)
        return self.get_triangles_and_convert_to_json(locations)

    def get_locations_within_radius_simple_json(self, lat, lng,
                                                radius_in_miles=5):
        """
        Gets all of the locations within the circle described by the point
        and radius of the circle.  Uses a simple search.
        Slow but cheap
        :param lat: float
        :param lng: float
        :param radius_in_miles: float *optional
        :return:
        """
        locations = PrivateLocation().get_locations_within_box(lat, lng,
                                                               radius_in_miles,
                                                               radius_in_miles)
        return self.get_triangles_and_convert_to_json(locations)

    def get_locations_by_zip(self, zip_code):
        locations = PrivateLocation().get_all_locations_by_zip(zip_code)
        return self.get_triangles_and_convert_to_json(locations)

    def get_triangles_and_convert_to_json(self, locations):
        """
        Gets triangles for locations and converts them to a json document
        :param locations: list of PrivateLocations
        :return: JSON document
        """
        triangles = list()
        for location in locations:
            triangles += self.get_triangles_for_location(location)
        return self.convert_locations_and_triangles_to_json(locations, triangles)

    def get_locations_that_contain_point_complex(self, lat, lng,
                                                 radius_in_miles=5):
        """
        Returns all of the locations that contain a given point. Using a
        complex API search.  Fast but expensive.
        :param lat: float
        :param lng: float
        :param radius_in_miles: float *optional
        :return: JSON document
        """
        locations = self.get_locations_within_radius_complex(lat, lng,
                                                             radius_in_miles)
        locations = self.get_locations_that_contain_point(locations, lat, lng)
        return self.convert_locations_and_triangles_to_json(locations=locations)

    def get_locations_that_contain_point_simple(self, lat, lng,
                                                radius_in_miles=5):
        """
        Returns all of the locations that contain a given point. Using a simple
        search.  Slow but cheap.
        :param lat:
        :param lng:
        :param radius_in_miles:
        :return: JSON document
        """
        locations = PrivateLocation().get_locations_within_box(lat, lng,
                                                               radius_in_miles,
                                                               radius_in_miles)
        locations = self.get_locations_that_contain_point(locations, lat, lng)
        return self.convert_locations_and_triangles_to_json(locations=locations)

    def get_locations_that_contain_point(self, locations, lat, lng):
        """
        Filters a list of locations and return the list of locations that
        contain that point
        :param locations: List of PrivateLocations
        :param lat: float
        :param lng: float
        :return: List of PrivateLocations
        """
        this_location = list()
        for location in locations:
            triangles = self.get_triangles_for_location(location)
            for triangle in triangles:
                if triangle.triangle.triangle_contains_coord(lat, lng):
                    this_location.append(location)
        return this_location

    def edit_location_with_polygon_change(self, new_polygon, pl_key):
        """
        Handles when a locations polygon has been change.  Removes the old
        triangles from the DB and remove the location from the index.  Then
        puts the new information in the DB and Index
        :param new_polygon: Polygon object
        :param pl_key: Key for PrivateLocation
        :return: Key for PrivateLocation
        """
        self.remove_location_triangles_and_index(pl_key)
        triangles = new_polygon.polygon_triangulation()
        for triangle in triangles:
            triangle_location = TriangleLocation()
            tl_key = triangle_location.create_location(pl_key,
                                                       triangle)
        pli = PrivateLocationIndex()
        pli.create_location(new_polygon.get_center_lat(),
                            new_polygon.get_center_lng(),
                            pl_key
                            )

        return pl_key

    @staticmethod
    def remove_location_triangles_and_index(pl_key):
        """
        Helper funtion to remove the children of a location from the
        TriagleLocation DB and PrivateLocationIndex
        :param pl_key:
        :return:
        """
        PrivateLocation().delete_location(pl_key)
        TriangleLocation().remove_triangles_for_private_location(pl_key)
        PrivateLocationIndex().delete_location(pl_key)