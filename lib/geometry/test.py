import random
import unittest
from lib.geometry import calculate_separating_vectors
from lib.geometry.util import generate_convex_hull, generate_random_polygon
from lib.geometry.polygon import Polygon
from lib.geometry.rect import Rect
from lib.vec2d import Vec2d
import sys, pygame

class GeometryTest(unittest.TestCase):
    def setUp(self):
        pass

    # def test_convex_hull_deterministic(self):
    #     length = None
    #     for i in range(100):
    #         points = [Vec2d(189, 442), Vec2d(189, 378), Vec2d(125, 378), Vec2d(125, 442), Vec2d(189, 350), Vec2d(189, 286), Vec2d(125, 286), Vec2d(125, 350), Vec2d(167, 346), Vec2d(167, 282), Vec2d(103, 282), Vec2d(103, 346), Vec2d(133, 376), Vec2d(133, 312), Vec2d(69, 312), Vec2d(69, 376), Vec2d(133, 442), Vec2d(133, 378), Vec2d(69, 378), Vec2d(69, 442)]
    #         num_points = len(generate_convex_hull(points))
    #         if length:
    #             self.assertEquals(num_points, length)
    #         else:
    #             length = num_points

#     def test_broken_hull_history1(self):
#         points = [Vec2d(60, 130), Vec2d(65, 83), Vec2d(105, 74), Vec2d(141, 136), Vec2d(79, 123)]
#         hull_points = generate_convex_hull(points)
#         self.assertEqual(hull_points, [Vec2d(141, 136), Vec2d(105, 74), Vec2d(65, 83), Vec2d(60, 130)])

#     def test_broken_hull_history2(self):
#         points = [Vec2d(105, 150), Vec2d(113, 134), Vec2d(84, 111), Vec2d(143, 137), Vec2d(136, 97), Vec2d(138, 60)]
#         hull_points = generate_convex_hull(points)
#         self.assertEqual(hull_points, [Vec2d(105, 150), Vec2d(143, 137), Vec2d(138, 60), Vec2d(84, 111)])

#     def test_broken_hull_history3(self):
#         points = [Vec2d(579, 518), Vec2d(500, 512), Vec2d(528, 501), Vec2d(573, 477), Vec2d(510, 541), Vec2d(533, 565), Vec2d(542, 578), Vec2d(516, 437), Vec2d(575, 401), Vec2d(519, 470)]
#         hull_points = generate_convex_hull(points)
#         self.assertEqual(len(hull_points), 6)

#     def test_convex_hull(self):
#         points = [Vec2d(1, 0), Vec2d(0, 0), Vec2d(0.5, 0.5),Vec2d(0, 1), Vec2d(1, 1)]
#         self.assertEqual(generate_convex_hull(points), [Vec2d(1, 1), Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 1)])

#     def test_contains_point(self):
#         polygon = Polygon([Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 1), Vec2d(1, 1)])
#         self.assertTrue(polygon.contains_point(Vec2d(0.5, 0.5)))
#         self.assertFalse(polygon.contains_point(Vec2d(2, 0)))
#         self.assertFalse(polygon.contains_point(Vec2d(1, 0)))
#         self.assertFalse(polygon.contains_point(Vec2d(0, 0)))
#         self.assertFalse(polygon.contains_point(Vec2d(0, 1)))
#         self.assertFalse(polygon.contains_point(Vec2d(1, 1)))

#     def test_contains_point2(self):
#         polygon = Polygon([Vec2d(270, 338), Vec2d(333, 336), Vec2d(338, 293), Vec2d(338, 229), Vec2d(289, 196), Vec2d(225, 196), Vec2d(190, 262), Vec2d(190, 326), Vec2d(206, 338)])
#         self.assertTrue(polygon.contains_point(Vec2d(241, 292)))
#         self.assertFalse(polygon.contains_point(Vec2d(396, 391)))

# class RectangleTest(unittest.TestCase):
#     def test_rect_raises(self):
#         self.assertRaises(ValueError, Rect, 0, 0, -4, 4)
#         self.assertRaises(ValueError, Rect, 0, 0, 4, -4)

#     def test_rect_intersect(self):
#         r1 = Rect(0, 0, 4, 4)
#         r2 = Rect(3, 4, 4, 4)
#         self.assertFalse(r1.intersects(r2))

#         r1 = Rect(0, 0, 4, 4)
#         r2 = Rect(3, 3, 4, 4)
#         self.assertTrue(r1.intersects(r2))

#         r1 = Rect(0, 0, 1, 1)
#         r2 = Rect(0, 0, 2, 2)
#         self.assertTrue(r1.intersects(r2))

class SeparatingAxisTest(unittest.TestCase):
    def assertSameElements(self, l_0, l_1):
        assert len(l_0) == len(l_1)
        assert len(set(l_0).intersection(set(l_1))) == len(l_0)

    # def test(self):
    #     points_0 = [Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 1), Vec2d(1, 1)]
    #     points_1 = [Vec2d(1.5, 0), Vec2d(0.5, 0), Vec2d(0.5, 1), Vec2d(1.5, 1)]
    #     result = calculate_separating_vectors(points_0, points_1)
    #     self.assertSameElements(result, [Vec2d(-0.5, 0), Vec2d(1.5, 0), Vec2d(0, 1), Vec2d(0, -1)])

    # def test_angled(self):
    #     points_0 = [Vec2d(0.5, -0.5), Vec2d(-0.5, 0.5), Vec2d(0.5, 1.5), Vec2d(1.5, 0.5)]
    #     points_1 = [Vec2d(1, 0), Vec2d(0, 1), Vec2d(1, 2), Vec2d(2, 1)]
    #     result = calculate_separating_vectors(points_0, points_1)
    #     self.assertSameElements(result, [Vec2d(-0.5, -0.5), Vec2d(-1.0, 1.0), Vec2d(1.0, -1.0), Vec2d(1.5, 1.5)])

    def test_non_overlapping(self):
        points_0 = [Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 1), Vec2d(1, 1)]
        points_1 = [Vec2d(3, 0), Vec2d(2, 0), Vec2d(2, 1), Vec2d(3, 1)]
        separating_vectors, overlaps = calculate_separating_vectors(points_0, points_1)
        self.assertFalse(overlaps)
        self.assertSameElements(separating_vectors, [])
    # def ztest_visual(self):
    #     pygame.init()
    #     size = width, height = 320, 240
    #     screen = pygame.display.set_mode(size, 0, 32)
    #     clock = pygame.time.Clock()

    #     black = (0, 0, 0)
    #     white = (255, 255, 255)
    #     green = (0, 255, 0)
    #     red = (255, 0, 0)
    #     bleh = (155, 10, 110)

    #     x_min = 50
    #     y_min = 50
    #     x_max = 100
    #     y_max = 100

    #     polygon = generate_random_polygon(x_min, y_min, x_max, y_max, 10)
    #     points = polygon.get_points()

    #     screen.fill(white)

    #     for point in points:
    #         draw_color = black
    #         pygame.draw.circle(screen, draw_color, (point.x, point.y), 3, 3)

    #     hull_points = generate_convex_hull(points, screen)

    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT: sys.exit()

    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_ESCAPE]:
    #             sys.exit()

    #         num_hull_points = len(hull_points)
    #         for i in range(num_hull_points):
    #             point_a = hull_points[(i + 1) % num_hull_points]
    #             point_b = hull_points[i]

    #             pygame.draw.line(screen, red, point_a, point_b)
    #             pygame.display.flip()

    #         pygame.display.flip()
    #         pygame.display.update()
    #         clock.tick(30)

if __name__ == '__main__':
    unittest.main()
