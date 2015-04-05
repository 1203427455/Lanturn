from lib.ecs.component.component import Component
from lib.vec2d import Vec2d

class PhysicsComponent(Component):
    component_id = 'PhysicsComponent'

    def __init__(self, entity):
        self.entity = entity
        self._velocity = Vec2d(0, 0)
        self._movement_velocity = Vec2d(0, 0)
        self._acceleration = Vec2d(0, 0)
        self.mass = 1
        self.forces = {}

    def get_total_velocity(self):
        return self.velocity + self.movement_velocity

    @property
    def movement_velocity(self):
        return self._movement_velocity.copy()

    @movement_velocity.setter
    def movement_velocity(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value')
        self._movement_velocity = val.copy()

    @property
    def velocity(self):
        return self._velocity.copy()

    @velocity.setter
    def velocity(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value')
        self._velocity = val.copy()

    @property
    def acceleration(self):
        return self._acceleration.copy()

    @acceleration.setter
    def acceleration(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value')
        self._acceleration = val.copy()

    def update_forces(self, delta):
        expired_forces = []
        for name, force in self.forces.iteritems():
            if not force.update(delta):
                expired_forces.append(name)

        for force in expired_forces:
            self.forces.pop(force)

    def get_net_force(self, exclude_forces=None):
        if exclude_forces is None:
            exclude_forces = []

        return (sum([force.vector for force_name, force in self.forces.iteritems()
            if force_name not in exclude_forces] or [Vec2d(0, 0)]))

class SkipGravityComponent(Component):
    component_id = 'SkipGravityComponent'

class ImmovableComponent(Component):
    component_id = 'ImmovableComponent'

class SkipCollisionResolutionComponent(Component):
    component_id = 'SkipCollisionResolutionComponent'
