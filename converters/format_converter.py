from shapes.point import Point


class FormatConverter:
    """This class handles converting the form of data from strings to points and vice versa"""

    @staticmethod
    def convert_points_string_to_points_list(points_string):
        """Takes as input a string point points separated by a '|' and the
        points are separated by a ','.  Returns a list of points
        """
        points = []
        points_string_list = points_string.split('|')
        for point_string in points_string_list:
            point_list = point_string.split(',')
            lat = float(point_list[0])
            lng = float(point_list[1])
            point = Point()
            point.set_point(lat, lng)
            points.append(point)
        return points