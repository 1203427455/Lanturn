from lib.ecs.component.shape import RectShapeComponent
from lib.geometry.rect import Rect
import pygame

class QuadTreeNode(object):
    def __init__(self, x, y, width, height, depth=0, max_count=4, max_depth=6):
        self.rect = Rect(x, y, width, height)
        self.entities = []
        self.children =[]
        self.depth = depth
        self.max_count = max_count
        self.max_depth = max_depth

        self.const_kwargs = {
            'max_count': max_count,
            'max_depth': max_depth
        }
        self.max_depth = max_depth

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, entity):
        return self.rect.intersects(entity[RectShapeComponent])

    def add_entity(self, entity):
        if self.intersects(entity):
            if self.children:
                for child in self.children:
                    child.add_entity(entity)
            else:
                self.entities.append(entity)
            if len(self.entities) > self.max_count and self.depth < self.max_depth:
                self.split()

    def remove_entity(self, entity):
        for child in self.children:
            child.remove_entity(entity)

        if entity in self.entities:
            self.entities.remove(entity)

    def split(self):
        child_width = int(self.width / 2.0)
        child_height = int(self.height / 2.0)

        top_left_child = QuadTreeNode(self.x,
            self.y,
            child_width,
            child_height,
            self.depth + 1,
            **self.const_kwargs
        )
        top_right_child = QuadTreeNode(
            self.x + child_width,
            self.y,
            self.width - child_width,
            child_height,
            self.depth + 1, **self.const_kwargs
        )
        bottom_left_child = QuadTreeNode(
            self.x,
            self.y + child_height,
            child_width,
            self.height - child_height,
            self.depth + 1,
            **self.const_kwargs
        )
        bottom_right_child = QuadTreeNode(
            self.x + child_width,
            self.y + child_height,
            self.width - child_width,
            self.height - child_height,
            self.depth + 1,
            **self.const_kwargs
        )

        self.children = [top_left_child, top_right_child, bottom_left_child, bottom_right_child]

        for child in self.children:
            for entity in self.entities:
                child.add_entity(entity)

        self.entities = []

    def get_intersections(self, entity):
        intersections = []

        for child in self.children:
            if child.intersects(entity):
                intersections.extend(child.get_intersections(entity))

        for _entity in self.entities:
            if _entity[RectShapeComponent].intersects(entity[RectShapeComponent]):
                intersections.append(_entity)

        return intersections

    def render(self, screen):
        color=(0, 115, 0)

        if self.children:
            pygame.draw.line(
                screen,
                color,
                (self.x + int(self.width / 2.0), self.y),
                (self.x + int(self.width / 2.0),
                self.y + self.height)
            )
            pygame.draw.line(
                screen,
                color,
                (self.x, self.y + int(self.height / 2.0)),
                (self.x + self.width,
                self.y + int(self.height / 2.0))
            )

        for child in self.children:
            child.render(screen)

    def print_node(self, indentation_level=0):
        if indentation_level == 0:
            print

        quadrants = ['top left', 'top right', 'bottom left', 'bottom right']
        indentation = '    ' * indentation_level

        for entity in self.entities:
            x, y = entity.position.x, entity.position.y
            width, height = entity[RectShapeComponent].width, entity[RectShapeComponent].height
            print '{}{}'.format(indentation, (x, y, width, height))

        for i, child in enumerate(self.children):
            new_indentation_level = indentation_level + 1
            print '{}[{} - ({}, {}) - {}x{}]'.format(
                '    ' * new_indentation_level,
                quadrants[i],
                child.rect.x,
                child.rect.y,
                child.rect.width,
                child.rect.height
            )
            child.print_node(new_indentation_level)
