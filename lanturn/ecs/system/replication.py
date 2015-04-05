import json
from lib.ecs.system.system import System
from lanturn.ecs.message_types import MESSAGE_TYPE
from lanturn.ecs.component.replication import ReplicationComponent

class ReplicationSystem(System):
    def __init__(self):
        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
            MESSAGE_TYPE.CLIENT_CONNECT: self.handle_client_connect,
        }
        self.entities = []
        self.clients = []

        super(ReplicationSystem, self).__init__(message_handlers)
    
    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(ReplicationComponent):
            self.entities.append(entity)

    def handle_client_connect(self, message):
        self.clients.append(message['connection'])

    def update(self, delta):
        self.handle_messages()
        for client in self.clients:
            message = [entity[ReplicationComponent].get_replication_data()
                for entity in self.entities]
            client.sendMessage(json.dumps(message))
