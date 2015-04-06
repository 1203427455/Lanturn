from collections import defaultdict
from lib.vec2d import Vec2d

class Entity(object):
    ID_GENERATOR = 0

    def __init__(self):
        self.id = self.ID_GENERATOR
        Entity.ID_GENERATOR += 1
        self._components = {}
        self._message_handlers = defaultdict(list)

    def __getitem__(self, component_class):
        return self._components[component_class.component_id]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def add_components(self, components):
        for component in components:
            self.add_component(component)

    def add_component(self, component):
        self._components[component.component_id] = component

    def get(self, component_class):
        return self._components.get(component_class.component_id)

    def send_message(self, message):
        pass