class SystemManager(object):
    instance = None
    
    def init(self, systems):
        self.systems = systems

    @staticmethod
    def get_instance():
        if SystemManager.instance is None:
            SystemManager.instance = SystemManager()

        return SystemManager.instance

    def send_message(self, message, immediate=False):
        for system in self.systems:
            system.send_message(message, immediate)

    def update(self, delta):
        for system in self.systems:
            if system.update(delta) is False:
                return False
