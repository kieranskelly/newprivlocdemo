from point import Point
from line import Line
from triangle import Triangle
import poly2tri


class Polygon:
    """Class describes a polygon using a list of ordered points
    on a cartesian plane
    """

    def __init__(self):
        self.polygon_points = []
        self.shear = 10

    def add_point_to_polygon(self, point):
        self.polygon_points.append(point)

    def create_polygon_by_points(self, points_list):
        for point in points_list:
            self.add_point_to_polygon(point)
        self.close_polygon()

    def close_polygon(self):
        if not self.polygon_points[0].point_is_equivalent(self.polygon_points[-1]):
            self.polygon_points.append(self.polygon_points[0])

    def get_max_lat(self):
        lats = [point.get_lat() for point in self.polygon_points]
        return max(lats)

    def get_min_lat(self):
        lats = [point.get_lat() for point in self.polygon_points]
        return min(lats)

    def get_max_lng(self):
        lats = [point.get_lng() for point in self.polygon_points]
        return max(lats)

    def get_min_lng(self):
        lats = [point.get_lng() for point in self.polygon_points]
        return min(lats)

    def get_center_lat(self):
        return (self.get_max_lat() + self.get_min_lat())/2.

    def get_center_lng(self):
        return (self.get_max_lng() + self.get_min_lng())/2.

    def get_center(self):
        return (self.get_center_lat(),self.get_center_lng())

    def polygon_is_equivalent(self, polygon):
        """Checks to see if current polygon has the same list of points
        as another polygon
        """
        if len(self.polygon_points) != len(polygon.polygon_points):
            return False
        for i in range(len(self.polygon_points)):
            if not self.polygon_points[i].point_is_equivalent(polygon.polygon_points[i]):
                return False
        return True

    def set_shear(self, shear):
        self.shear = shear

    def get_shear(self):
        return self.shear

    def is_valid_polygon(self):
        """Checks to see if the current polygon has at least three distinct
        points, that the first and last points are the same, and that the
        polygon does not cross over itself
        """
        if len(self.polygon_points) < 4:
            return False
        if not self.polygon_points[0].point_is_equivalent(self.polygon_points[-1]):
            return False
        line1 = Line()
        line2 = Line()
        for i in range(len(self.polygon_points)-1):
            line1.set_line_by_points(self.polygon_points[i],
                                     self.polygon_points[i+1])
            for j in range(i+1, len(self.polygon_points)-1):
                line2.set_line_by_points(self.polygon_points[j],
                                         self.polygon_points[j+1])
                if line1.do_lines_intersect(line2):
                    return False
        return True

    def polygon_triangulation(self):
        """returns a list of triangles that describe the current polygon"""
        self.close_polygon()
        poly_line = []
        triangles = []
        for point in self.polygon_points:
            poly_line.append(point.get_point())
        this_polygon = None
        for i in range(5):
            try:
                this_polygon = poly2tri.Triangulator(poly_line)
                break
            except:
                pass
        if not this_polygon:
            return None
        for triangle in this_polygon.polygons:
            point_a = Point()
            point_a.set_point(triangle[0].x, triangle[0].y)
            point_b = Point()
            point_b.set_point(triangle[1].x, triangle[1].y)
            point_c = Point()
            point_c.set_point(triangle[2].x, triangle[2].y)
            this_triangle = Triangle()
            this_triangle.set_points_by_point(point_a,
                                              point_b,
                                              point_c)
            triangles.append(this_triangle)
        return triangles