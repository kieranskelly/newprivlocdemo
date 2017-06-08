from handlers.enhanced_handler import EnhancedHandler
from managers.location_management import LocationManagement


class LocationsWithinRadius(EnhancedHandler):
    """
    Class handles search requests for all locations within the radius of a point.
    """
    def get(self):
        lat = self.request.get('lat')
        lng = self.request.get('lng')
        radius = self.request.get('radius')
        search_type = self.request.get('search')
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except:
            self.bad_search()
            return
        lm = LocationManagement()
        if search_type == 'complex':
            results = lm.get_locations_within_radius_complex_json(lat,
                                                                  lng,
                                                                  radius)
        else:
            results = lm.get_locations_within_radius_simple_json(lat,
                                                                 lng,
                                                                 radius)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(results)


class LocationsThatContainPoint(EnhancedHandler):
    """
    Class handles returning all of the locations that contain a given point
    """
    def get(self):
        lat = self.request.get('lat')
        lng = self.request.get('lng')
        search_type = self.request.get('search')
        try:
            lat = float(lat)
            lng = float(lng)
        except:
            self.bad_search()
            return
        lm = LocationManagement()
        if search_type == 'complex':
            results = lm.get_locations_that_contain_point_complex(lat, lng)
        else:
            results = lm.get_locations_that_contain_point_simple(lat, lng)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(results)


class LocationsThatContainPointUsingMap(EnhancedHandler):
    """
    Class handles rendering the map and then routes
    the query to LocationsThatContainPoint
    """
    def get(self):
        self.add_page_name('within_location')
        self.render('location_query_form.html', **self.arg_dict)

    def post(self):
        lat = self.request.get('lat')
        lng = self.request.get('long')
        try:
            lat = float(lat)
            lng = float(lng)
        except:
            return
        lat_long = 'lat=' + str(lat) + '&lng=' + str(lng)
        comp = '&search=complex'
        self.redirect('/within_location?' + lat_long + comp)
        return


class LocationsNearbyUsingMap(EnhancedHandler):
    """
    Class handles rendering the map and then routes
    the query to LocationsWithinRadius
    """
    def get(self):
        self.add_page_name('nearby_locations')
        self.render('location_query_form.html', **self.arg_dict)

    def post(self):
        lat = self.request.get('lat')
        lng = self.request.get('long')
        try:
            lat = float(lat)
            lng = float(lng)
        except:
            return
        lat_long = 'lat=' + str(lat) + '&lng=' + str(lng)
        rad = '&radius=5'
        comp = '&search=complex'
        self.redirect('/radius?' + lat_long + rad + comp)
        return


class LocationsWithinZipCode(EnhancedHandler):
    def get(self):
        zip_code = self.request.get('zipCode')
        lm = LocationManagement()
        results = lm.get_locations_by_zip(zip_code)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(results)
        return