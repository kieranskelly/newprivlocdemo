from google.appengine.api import search


class PrivateLocationIndex:
    """Class creates an interface to create and search for documents in with
    the Google Search API.
    """
    def __init__(self):
        self.index_name = 'private_location_index'

    @staticmethod
    def convert_pl_key_to_string(pl_key):
        return str(pl_key.id())

    @staticmethod
    def miles_to_meters(miles):
        return int(1609.34 * miles)

    def create_location_by_private_location(self, private_location):
        """
        Uses the create location function to create a search document using
        a private location
        :param private_location: private location object
        :return: Boolean of whether the location was inserted
        """
        center_lat = private_location.polygon.get_center_lat()
        center_lng = private_location.polygon.get_center_lng()
        private_location_fk_str = self\
            .convert_pl_key_to_string(private_location.key)
        return self.create_location(center_lat,
                                    center_lng,
                                    private_location_fk_str)

    def create_location(self, center_lat, center_lng, pl_key):
        """
        Creates a search document.
        :param center_lat: float representing the center latitude
        :param center_lng: float representing the center longitude
        :param pl_key: key property of the private location
        :return: Boolean of whether the location was inserted
        """
        geo_point = search.GeoPoint(center_lat, center_lng)
        private_location_fk_str = self\
            .convert_pl_key_to_string(pl_key)
        fields = list()
        fields.append(search.GeoField(name='center', value=geo_point))
        fields.append(search.AtomField(name='private_location_id',
                                       value=private_location_fk_str))
        d = search.Document(fields=fields)
        index = search.Index(name=self.index_name)
        add_result = index.put(d)
        return add_result

    def delete_location(self, pl_key):
        private_location_key_str = self\
            .convert_pl_key_to_string(pl_key)
        query = private_location_key_str
        index = search.Index(self.index_name)
        while True:
            search_results = index.search(query)
            doc_ids = [doc.doc_id for doc in search_results]
            if not doc_ids:
                break
            index.delete(doc_ids)

    def get_location_by_pl_key(self, pl_key):
        index = search.Index(self.index_name)
        query = 'private_location_id' + self.convert_pl_key_to_string(pl_key)
        results = index.search(query)
        return results

    def get_locations_within_radius(self, radius_in_miles,
                                    lat, lng, results_limit=1000):
        """
        Search the index for all locations that are within the perimeter of
        a circle a described but a point and radius
        :param radius_in_miles: float The radius of the search circle
        :param lat: float The latitude of a point
        :param lng: float The Longitude of a point
        :param results_limit: Current not used, defaults to Google default
        :return: Iterable of all locations within the circle
        """
        meters = self.miles_to_meters(radius_in_miles)
        query = "distance(%s, geopoint(%f, %f)) < %i" \
                % ('center', lat, lng, meters)
        loc_expr = "distance(center, geopoint(%f, %f))" % (lat, lng)
        sort_expr = search.SortExpression(expression=loc_expr,
                                         direction=search.SortExpression.ASCENDING,
                                         default_value=meters+1)
        search_query = search.Query(query_string = query,
                            options = search.QueryOptions(
                            sort_options = search.SortOptions(expressions=[sort_expr])))
        search_result = search.Index(self.index_name).search(search_query)
        return search_result