from point import Point


class Line:
    """
    Class creates an object that represents a line segment
    """
    def __init__(self):
        self.point_a = Point()
        self.point_b = Point()

    def set_line_by_points(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def set_line_by_coord(self, point_a_lat, point_a_lng,
                          point_b_lat, point_b_lng):
        point_a = Point()
        point_a.set_point(point_a_lat, point_a_lng)
        point_b = Point()
        point_b.set_point(point_b_lat, point_b_lng)
        self.set_line_by_points(point_a, point_b)

    def get_point_a(self):
        return self.point_a

    def get_point_b(self):
        return self.point_b

    def get_length(self):
        delta_lat = self.get_point_a().get_lat() - self.get_point_b().get_lat()
        delta_lng = self.get_point_a().get_lng() - self.get_point_b().get_lng()
        return (delta_lat**2 + delta_lng**2)**.5

    def get_slope(self):
        delta_x = self.get_point_b().get_lat() - self.get_point_a().get_lat()
        delta_y = self.get_point_b().get_lng() - self.get_point_a().get_lng()
        if delta_x == 0:
            return float('inf')
        return delta_y/delta_x

    def do_lines_share_node(self, other_line):
        """
        Helper function to see is two lines share a node
        :param other_line: Line object
        :return: Boolean
        """
        if self.get_point_a().point_is_equivalent(other_line.get_point_a()) or\
            self.get_point_a().point_is_equivalent(other_line.get_point_b()) or\
            self.get_point_b().point_is_equivalent(other_line.get_point_a()) or\
            self.get_point_b().point_is_equivalent(other_line.get_point_b()):
            return True
        else:
            return False

    def do_connected_lines_overlap(self, other_line):
        """
        Helper function checks to see if two connected lines overlap
        ie. [(0,0),(2,0)] overlaps [(2,0),(1,0)]
        but [(0,0),(2,0)] does not overlap [(2,0),(1,1)]
        :param other_line: Line object
        :return: Boolean
        """
        if self.get_slope() != other_line.get_slope():
            return False
        a = self.get_point_a()
        b = self.get_point_b()
        x = other_line.get_point_a()
        y = other_line.get_point_b()
        if a.point_is_equivalent(y):
            x, y = y, x
        elif b.point_is_equivalent(x):
            a, b = b, a
        if a.point_is_equivalent(x) and b.point_is_equivalent(y):
            return True
        if self.get_length() <= other_line.get_length:
            a, b, x, y = x, y, a, b
        return y.point_is_between(a, b)

    def bounding_box(self):
        min_lat = self.get_point_a().get_lat()
        max_lat = self.get_point_b().get_lat()
        min_lng = self.get_point_a().get_lng()
        max_lng = self.get_point_b().get_lng()
        if min_lat > max_lat:
            min_lat, max_lat = max_lat, min_lat
        if min_lng > max_lng:
            min_lng, max_lng = max_lng, min_lng
        return min_lat, max_lat, min_lng, max_lng


    def do_bounding_boxes_intersect(self, other_line):
        a1,a2,b1,b2 = self.bounding_box()
        x1,x2,y1,y2 = other_line.bounding_box()
        return a1 <= x2 and a2 >= x1 and b1 <= y2 and b2 >= y1

    def do_line_and_extended_line_cross(self, other_line):
        new_a = Line()
        new_a.set_line_by_coord(0,0,
                   self.get_point_b().get_lat() - self.get_point_a().get_lat(),
                   self.get_point_b().get_lng() - self.get_point_a().get_lng())
        new_b = Line()
        new_b.set_line_by_coord(
             other_line.get_point_a().get_lat() - self.get_point_a().get_lat(),
             other_line.get_point_a().get_lng() - self.get_point_a().get_lng(),
             other_line.get_point_b().get_lat() - self.get_point_a().get_lat(),
             other_line.get_point_b().get_lng() - self.get_point_a().get_lng())
        return not ((self.crossproduct(new_a, new_b.get_point_a()) and \
                self.crossproduct(new_a, new_b.get_point_b())) or \
               (self.crossproduct(new_b, new_a.get_point_a()) and \
                self.crossproduct(new_b, new_a.get_point_b())))

    def crossproduct(self, line, point):
        xproduct = ((point.get_lng() - line.get_point_a().get_lng()) * \
                (line.get_point_b().get_lat() - line.get_point_a().get_lat())) - \
                ((point.get_lat() - line.get_point_a().get_lat()) * \
                (line.get_point_b().get_lng() - line.get_point_a().get_lng()))
        return xproduct < 0


    def do_lines_intersect(self, other_line):
        #check if the segments share a node
        if self.do_lines_share_node(other_line):
            return self.do_connected_lines_overlap(other_line)
        a = self.get_point_a()
        b = self.get_point_b()
        x = other_line.get_point_a()
        y = other_line.get_point_b()
        #if bounding boxes do not intersect segments do not intersect
        if not self.do_bounding_boxes_intersect(other_line):
            return False
        #check to see if any end point is contained in the other segment
        if a.point_is_between(x,y) or b.point_is_between(x,y) or \
            x.point_is_between(a,b) or y.point_is_between(a,b):
            return True
        return self.do_line_and_extended_line_cross(other_line)

