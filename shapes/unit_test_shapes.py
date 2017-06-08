from point import Point
from line import Line
from polygon import Polygon

point00 = Point()
point00.set_point(0,0)
point01 = Point()
point01.set_point(0,1)
point10 = Point()
point10.set_point(1,0)
point11 = Point()
point11.set_point(1,1)
point55 = Point()
point55.set_point(5,5)
pointm1m1 = Point()
pointm1m1.set_point(-1,-1)

line1 = Line()
line2 = Line()

def print_line(line):
    print str(line.get_point_a().get_coord())+"-->"+\
          str(line.get_point_b().get_coord())

def do_lines(point_a, point_b, point_x, point_y):
    line1.set_line_by_points(point_a, point_b)
    print_line(line1)
    line2.set_line_by_points(point_x, point_y)
    print_line(line2)
    print line1.do_lines_intersect(line2)

print "SB True"
do_lines(point00, point11, point01, point10)
print ""

print "SB False"
do_lines(point00, point11, point00, pointm1m1)
print ""

print "SB False"
do_lines(point00, point11, pointm1m1, point00)
print ""

print "SB True"
do_lines(point00, point55, point01, point11)
print ""

print "SB True"
do_lines(pointm1m1, point55, point00, point11)
print ""

print "SB False"
do_lines(point00, point01, point10, point11)
print ""

point_a = Point()
point_b = Point()
point_c = Point()
point_d = Point()
point_e = Point()
point_a.set_point(37.451452511976484, -122.1852757036686)
point_b.set_point(37.451342851801144, -122.18536891043186)
point_c.set_point(37.45119007255098, -122.18509197235107)
point_d.set_point(37.451303459271735, -122.18499675393105)
point_e.set_point(37.451452511976484, -122.1852757036686)
counter = 0
p = Polygon()
p.create_polygon_by_points([point_a, point_b, point_c, point_d, point_a])
print p.is_valid_polygon()
print 'done'
triangles = p.polygon_triangulation()
for triangle in triangles:
    print triangle.point_a.get_lat(),triangle.point_a.get_lng(),triangle.point_b.get_lat(),triangle.point_b.get_lng()