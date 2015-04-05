from lib.ecs.component.component import Component
from lib.geometry.util import generate_random_polygon, generate_convex_hull, copy_points_list
from lib.geometry.polygon import Polygon
from lib.vec2d import Vec2d

class ShapeComponent(Component):
    component_id = 'ShapeComponent'

    def __init__(self, entity, x_max, y_max, max_points):
        self.polygon = generate_random_polygon(x_max, y_max, max_points)
        self.entity = entity

    def get_points(self):
        return [self.entity.position + point for point in self.polygon.get_points()]

    #TODO : this method should be in Polygon.  Have this method create a new polygon
    # that has been offsetted by the entity's position
    def compute_c_polygon(self, agent):
        agent_points = copy_points_list(agent.get_points())

        all_points = []
        for point in self.get_points():
            for agent_point in agent_points:
                all_points.append(point - agent_point)

        c_polygon_points = generate_convex_hull(all_points)
        return Polygon(c_polygon_points)

class DefinedShapeComponent(Component):
    component_id = ShapeComponent.component_id

    def __init__(self, entity, points):
        self.entity = entity
        self.points = points

    def get_points(self):
        return [self.entity.position + point for point in self.points]

class RectShapeComponent(Component):
    component_id = ShapeComponent.component_id

    def __init__(self, entity, width, height):
        self.entity = entity
        self.width, self.height = width, height

    def get_min_max(self):
        min_x, min_y = self.entity.position[0], self.entity.position[1]
        max_x = self.entity.position[0] + self.width - 1
        max_y = self.entity.position[1] + self.height - 1

        return min_x, max_x, min_y, max_y

    def intersects(self, other):
        self_min_x, self_max_x, self_min_y, self_max_y = self.get_min_max()
        other_min_x, other_max_x, other_min_y, other_max_y = other.get_min_max()

        return not (any([self_min_x > other_max_x, self_max_x < other_min_x,
            self_min_y > other_max_y, self_max_y < other_min_y]))

    def get_points(self):
        min_x, max_x, min_y, max_y = self.get_min_max()

        points = [
            Vec2d(max_x, min_y),
            Vec2d(min_x, min_y),
            Vec2d(min_x, max_y),
            Vec2d(max_x, max_y),
        ]

        return points
