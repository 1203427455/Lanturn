from lib.ecs.system.system import System
from lanturn.ecs.message_types import MESSAGE_TYPE

class EffectSystem(System):
    def __init__(self):
        message_handlers = {
            # MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        super(EffectSystem, self).__init__(message_handlers)
    
