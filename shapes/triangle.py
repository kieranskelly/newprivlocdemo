from point import Point


class Triangle:
    """Class describes the 3 three points of a triangle on a cartesian plane"""

    def __init__(self):
        self.point_a = Point()
        self.point_b = Point()
        self.point_c = Point()
        self.tolerance = .0001

    def set_points_by_point(self, point_a, point_b, point_c):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c

    def set_points(self, point_a_lat, point_a_lng,
                    point_b_lat, point_b_lng,
                    point_c_lat, point_c_lng):
        point_a = Point()
        point_a.set_point(point_a_lat, point_a_lng)
        point_b = Point()
        point_b.set_point(point_b_lat, point_b_lng)
        point_c = Point()
        point_c.set_point(point_c_lat, point_c_lng)
        self.set_points_by_point(point_a, point_b, point_c)

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def get_tolerance(self):
        return self.tolerance

    def get_points(self):
        points = list()
        points.append(self.point_a.get_point())
        points.append(self.point_b.get_point())
        points.append(self.point_c.get_point())
        return points

    @staticmethod
    def area_of_a_triangle(point_one, point_two, point_three):
        lat_one = point_one.get_lat()
        lng_one = point_one.get_lng()
        lat_two = point_two.get_lat()
        lng_two = point_two.get_lng()
        lat_three = point_three.get_lat()
        lng_three = point_three.get_lng()
        area = (lng_one*(lat_two-lat_three) +
                lng_two*(lat_three-lat_one) +
                lng_three*(lat_one-lat_two))/2.
        return abs(area)

    def triangle_contains_point(self, point):
        """Checks to see if a point is within the boundaries of the triangle"""
        if self.point_a is None or \
           self.point_b is None or \
           self.point_c is None:
            return None
        total_area = self.area_of_a_triangle(self.point_a,
                                             self.point_b,
                                             self.point_c)
        area_one = self.area_of_a_triangle(self.point_a, self.point_b, point)
        area_two = self.area_of_a_triangle(self.point_a, point, self.point_c)
        area_three = self.area_of_a_triangle(point, self.point_b, self.point_c)
        return abs(area_one + area_two + area_three - total_area) < \
                total_area*self.tolerance

    def triangle_contains_coord(self, lat, lng):
        """Checks to see if the lat and lng are contained within the boundaries
        of the triangle
        """
        point = Point()
        point.set_point(lat, lng)
        return self.triangle_contains_point(point)

    def get_max_lat(self):
        return max(self.point_a.get_lat(),
                   self.point_b.get_lat(),
                   self.point_c.get_lat())

    def get_min_lat(self):
        return min(self.point_a.get_lat(),
                   self.point_b.get_lat(),
                   self.point_c.get_lat())

    def get_max_lng(self):
        return max(self.point_a.get_lng(),
                   self.point_b.get_lng(),
                   self.point_c.get_lng())
    
    def get_min_lng(self):
        return min(self.point_a.get_lng(),
                   self.point_b.get_lng(),
                   self.point_c.get_lng())