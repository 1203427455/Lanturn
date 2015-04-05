from lib.ecs.component.component import Component

class InputComponent(Component):
    component_id = 'InputComponent'

    def __init__(self, entity):
        self.entity = entity

class KeyboardInputComponent(InputComponent):
    def __init__(self, entity):
        self.entity = entity
        self.keys = {}

    def bind(self, key, command):
        self.keys[key] = command

    def keydown_event(self, key):
        if self.keys.get(key):
            self.keys[key].execute(self.entity)

    def keyup_event(self, key):
        if self.keys.get(key):
            self.keys[key].undo(self.entity)
