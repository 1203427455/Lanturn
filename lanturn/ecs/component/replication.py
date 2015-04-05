from lib.ecs.component.component import Component

class ReplicationComponent(object):
	component_id = 'ReplicationComponent'
	def __init__(self, entity):
		self.entity = entity

class PlayerReplicationComponent(ReplicationComponent):
	def get_replication_data(self):
		return {
			'id': self.entity.id,
			'position': (self.entity.position[0], self.entity.position[1]),
			'orientation': self.entity.orientation
		}