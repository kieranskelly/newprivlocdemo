from point import Point
import math

#radius of earth
RADIUS = 1


class Circle:
    """
    Not currently implemented or working
    """

    def __init__(self):
        self.center = None
        self.radius = None

    def set_center_by_point(self, point):
        self.center = point

    def set_center_by_coord(self, lat, lng):
        point = Point()
        point.set_point(lat, lng)
        self.set_center_by_point(point)

    def set_radius(self, radius):
        self.radius = radius

    def set_circle_by_coord(self, lat, lng, radius):
        self.set_center_by_coord(lat,lng)
        self.set_radius(radius)

    def set_circle_by_point(self, point, radius):
        self.set_center_by_point(point)
        self.set_radius(radius)

    def get_center(self):
        return self.center.get_point()

    def get_radius(self):
        return self.radius

    def get_circle(self):
        return (self.get_center(), self.radius)

    def is_point_within_circle(self, point):
        ew_dist = 2. * math.pi * RADIUS * math.cos(self.center.get_lat())*\
            (point.get_lng() - self.center.get_lng())/360.
        ns_dist = 2 * math.pi * RADIUS * (point.get_lat() - 
                                          self.center.get_lat())/360.
        D = math.sqrt(math.pow(ew_dist,2) + math.pow(ns_dist,2))
        return D <= self.radius
