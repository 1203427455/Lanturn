import unittest
from lib.quad_tree.quad_tree import QuadTreeNode
from lib.ecs.entity.entity import Entity
from lib.ecs.component.shape import RectShapeComponent


class QuadTreeTest(unittest.TestCase):
    def setUp(self):
        pass

    def create_entity(self, x, y, width, height):
        entity = Entity(x, y)
        entity.set_component(RectShapeComponent(entity, width, height))
        return entity

    def test_add(self):
        node = QuadTreeNode(0, 0, 5, 5, max_count=2)

        node.add_entity(self.create_entity(0, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 1, 1))

        self.assertEquals(len(node.children), 0)
        self.assertEquals(len(node.entities), 2)

    def test_split(self):
        node = QuadTreeNode(0, 0, 5, 5, max_count=2)

        node.add_entity(self.create_entity(0, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 3, 3))

        self.assertEquals(len(node.children), 4)
        self.assertEquals(len(node.entities), 0)
        self.assertEquals(len(node.children[0].children), 4)

    def test_add_to_sub_node(self):
        node = QuadTreeNode(0, 0, 5, 5, max_count=2)

        node.add_entity(self.create_entity(0, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 3, 3))
        self.assertEquals(len(node.children[0].children[0].entities), 1)

        node.add_entity(self.create_entity(0, 0, 1, 1))

        self.assertEquals(len(node.children), 4)
        self.assertEquals(len(node.entities), 0)
        self.assertEquals(len(node.children[0].children[0].entities), 2)

    def test_remove(self):
        node = QuadTreeNode(0, 0, 5, 5, max_count=2)

        node.add_entity(self.create_entity(0, 0, 1, 1))
        node.add_entity(self.create_entity(1, 0, 1, 1))

        sub_child_entity = self.create_entity(1, 0, 3, 3)
        node.add_entity(sub_child_entity)
        self.assertEquals(len(node.children[3].entities), 1)
        node.remove_entity(sub_child_entity)
        self.assertEquals(len(node.children[3].entities), 0)


if __name__ == '__main__':
    unittest.main()
