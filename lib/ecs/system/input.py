import pygame

from lib.ecs.system.system import System
from lib.ecs.component.input import InputComponent, KeyboardInputComponent

from lanturn.ecs.message_types import MESSAGE_TYPE

class InputSystem(System):
    def __init__(self):
        self.entities = []

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        super(InputSystem, self).__init__(message_handlers)

    def game_over(self):
        raise Exception('GAME OVER')

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(InputComponent):
            self.entities.append(entity)
            # keyboard_input_component = entity[KeyboardInputComponent]
            # keyboard_input_component.keydown_event(pygame.K_a)

    def update(self, delta):
        self.handle_messages()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                for entity in self.entities:
                    keyboard_input_component = entity[KeyboardInputComponent]
                    keyboard_input_component.keydown_event(event.key)
            elif event.type == pygame.KEYUP:
                for entity in self.entities:
                    keyboard_input_component = entity[KeyboardInputComponent]
                    keyboard_input_component.keyup_event(event.key)
            elif event.type == pygame.QUIT:
                return False
