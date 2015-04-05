import random
import pygame
from lib.vec2d import Vec2d

EPSILON = 0.02

def line_segment_equal(line_a, line_b):
    return (line_a[0] == line_b[0] and line_a[1] == line_b[1]) or (line_a[0] == line_b[1] and line_a[1] == line_b[0])

def line_in_polygon(line, polygon):
    for edge in polygon.get_edges():
        if line_segment_equal(edge, line):
            return True
    return False

def distance_between(node_a, node_b):
    point_a = Vec2d(node_a.x, node_a.y)
    point_b = Vec2d(node_b.x, node_b.y)

    return (point_a - point_b).get_length()

def polygons_intersect(polygon_a, polygon_b):
    for edge in polygon_a.get_edges():
        if intersect_polygon(edge, polygon_b):
            return True

    return False

def intersect_polygons(line_segment, polygons):
    for polygon in polygons:
        if intersect_polygon(line_segment, polygon):
            return True
    return False

def intersect_polygon(line_segment, polygon):
    if line_in_polygon(line_segment, polygon):
        return False

    shared_points = 0
    for edge in polygon.get_edges():
        if shares_point(line_segment, edge):
            shared_points += 1

    # Both points in the line is in the polygon yet they're not on the same line segment
    # This is considered an intersection
    if shared_points > 2:
        return True

    for edge in polygon.get_edges():
        if line_intersect(line_segment, edge, True):
            return True

    return False

def shares_point(line_a, line_b):
    return (line_a[0] == line_b[0]) or (line_a[1] == line_b[1]) or (line_a[0] == line_b[1]) or (line_a[1] == line_b[0])

def shares_point2(t_value_a, t_value_b):
    if (t_value_a in (0, 1)) and (t_value_b in (0, 1)):
        return True
    else:
        return False

def line_intersect(line_a, line_b, ignore_overlapping=False):
    line_a_t_value = _compute_t_value(line_a, line_b)

    # Co Linear lines
    if ignore_overlapping and line_a_t_value is None:
        return False

    if (line_a_t_value < (0 - EPSILON)) or (line_a_t_value >  (1 + EPSILON)):
        return False

    line_b_t_value = _compute_t_value(line_b, line_a)

    if (line_b_t_value < (0 - EPSILON)) or (line_b_t_value >  (1 + EPSILON)):
        return False

    if shares_point2(line_a_t_value, line_b_t_value):
        return False

    if shares_point(line_a, line_b):
        if shares_point(line_a, line_b) != shares_point2(line_a_t_value, line_b_t_value):
            print 'WAHH DID NOT ExPECT TO HIT THIS {}, {}'.format(line_a_t_value, line_b_t_value)
            print line_a, line_b
            print 'shared_point1 {}'.format(shares_point(line_a, line_b))
            print 'shares_point2 {}'.format(shares_point2(line_a_t_value, line_b_t_value))

        return False

    return True

def _compute_t_value(intersector, intersectee):
    intersectee_dir = intersectee[1] - intersectee[0]
    normal = Vec2d(intersectee_dir[1], -intersectee_dir[0])

    A = intersector[0]
    B = intersector[1]
    P = intersectee[0]

    denominator = (A - B).dot(normal)

    if denominator == 0:
        return None

    return (A - P).dot(normal) / denominator

def create_polygons(vertex_lists):
    from lib.geometry.polygon import Polygon
    polygons = []
    for vertex_list in vertex_lists:
        polygons.append(Polygon(vertex_list))

    return polygons

def generate_random_polygon(x_max, y_max, max_points):
    from lib.geometry.polygon import Polygon

    points = []

    i = 0
    while i < max_points:
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)

        if Vec2d(x, y) in points:
            continue
        else:
            points.append(Vec2d(x, y))
            i += 1

    hull_points = generate_convex_hull(points)
    return Polygon(hull_points)

def get_bottom_right_most_point(points):
    lowest_point = points[0]

    for point in points:
        if point.y > lowest_point.y:
            lowest_point = point
        elif point.y == lowest_point.y:
            if point.x > lowest_point.x:
                lowest_point = point

    return lowest_point

def generate_convex_hull(points, screen=None):
    # Note, this algorithm requires that we select the bottom most point.
    # Otherwise, we could potentially get negative angles from `get_angle_between()`
    # which throws off the angle sorting

    if len(points) < 3:
        raise Exception('Cannot generate convex hull for fewer than three points')

    pivot_point = get_bottom_right_most_point(points)
    point_to_angle_map = {}
    for point in points:
        if point == pivot_point:
            continue

        angle = Vec2d(pivot_point.x + 1, pivot_point.y).get_angle_between(point - pivot_point)
        if angle < 0:
            angle += 360

        point_to_angle_map[point] = angle

    sorted_points = sorted(point_to_angle_map.iteritems(), key=lambda tuple: (tuple[1], tuple[0].get_distance(pivot_point)), reverse=True)
    sorted_points = [x[0] for x in sorted_points]
    sorted_points.append(pivot_point)

    hull_points = [pivot_point, sorted_points[0], sorted_points[1]]

    for point in sorted_points[2:]:
        next_hull_point_found = False
        while not next_hull_point_found:
            previous, current, next = hull_points[-3:]
            vec2 = next - current
            vec1 = current - previous

            if vec2.cross(vec1) > 0:
                hull_points.append(point)
                next_hull_point_found = True
            elif vec2.cross(vec1) < 0:
                hull_points.pop(-2)
            else:
                next_dist = (next - previous).get_length()
                current_dist = (current - previous).get_length()

                # Keep the point that's further away for our convex hull
                if next_dist > current_dist:
                    hull_points.pop(-2)
                else:
                    hull_points.pop()
                
                hull_points.append(point)
                next_hull_point_found = True

    hull_points.pop()

    return hull_points

def copy_points_list(points):
    return [point.copy() for point in points]
