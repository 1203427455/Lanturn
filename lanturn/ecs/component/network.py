from lib.ecs.component.component import Component

class NetworkComponent(object):
    component_id = 'NetworkComponent'
    def __init__(self, connection):
        self.connection = connection