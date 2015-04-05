class System(object):
    def __init__(self, message_handlers):
        self.messages = []
        self.message_handlers = message_handlers

    def send_message(self, message, immediate=False):
        if immediate:
            message_type = message['message_type']
            if message_type in self.message_handlers.keys():
                self.message_handlers[message_type](message)
        else:
            self.messages.append(message)

    def update(self, delta):
        return

    def get_message_handlers(self):
        return self.message_handlers

    def handle_messages(self):
        for message in self.messages:
            message_type = message['message_type']
            if message_type not in self.message_handlers.keys():
                continue
            self.message_handlers[message_type](message)

        self.messages = []
