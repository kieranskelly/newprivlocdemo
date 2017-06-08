

class Point():
    """Class describes a point in a cartesian plane"""

    def __init__(self):
        self.lat = None
        self.lng = None

    def set_lat(self, lat):
        self.lat = float(lat)

    def set_lng(self, lng):
        self.lng = float(lng)

    def set_point(self, lat, lng):
        self.set_lat(lat)
        self.set_lng(lng)

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng

    def get_coord(self):
        return (self.lat, self.lng)

    def get_point(self):
        return self.get_lat(), self.get_lng()

    def point_exists(self):
        if self.lat <> None and self.lng <> None:
            return True
        return False
    
    def point_is_equivalent(self, other_point):
        """Compares a point with current point to see if they have the same
        latitude and longitude returns True if points are the same False if not
        """
        if self.get_coord() == other_point.get_coord():
            return True
        else:
            return False

    def point_is_between(self, point_a, point_b, epsilon = None):
        """Checks to see if current point lies on a segment described by
        point_a and point_b.
        """
        if epsilon is None:
            epsilon = .00000000000000001
        crossproduct = ((self.get_lng() - point_a.get_lng()) * \
                        (point_b.get_lat() - point_a.get_lat())) - \
                        ((self.get_lat() - point_a.get_lat()) * \
                        (point_b.get_lng() - point_a.get_lng()))
        if abs(crossproduct) > epsilon:
            return False
        dotproduct = ((self.get_lat() - point_a.get_lat()) * \
                     (point_b.get_lat() - point_a.get_lat())) + \
                     ((self.get_lng() - point_a.get_lng()) * \
                     (point_b.get_lng() - point_a.get_lng()))
        if dotproduct < 0:
            return False
        sq_length_ab = (point_b.get_lat() - point_a.get_lat())**2 + \
                       (point_b.get_lng() - point_a.get_lng())**2
        if dotproduct > sq_length_ab:
            return False
        return True

