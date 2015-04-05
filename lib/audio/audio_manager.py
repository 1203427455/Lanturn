from lib.resource_manager import ResourceManager

class AudioManager(object):
    instance = None
    resource_manager = ResourceManager.get_instance()

    @staticmethod
    def get_instance():
        if AudioManager.instance is None:
            AudioManager.instance = AudioManager()

        return AudioManager.instance

    def play(self, name):
        audio = self.resource_manager.get_audio(name)
        if audio:
            audio.play()
