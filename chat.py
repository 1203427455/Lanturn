class ChatService(object):
    message_id = 0

    def __init_(self):
        self.rooms = defaultdict()

    def create_room(self, client_ids):
        room_id = '-'.join(sorted(client_ids))
        self.rooms[room_id] = []
        return room_id

    def send_message(self, room_id, sender_id, message):
        room = self.rooms[room_id]
        room.append({
            'sender_id': sender_id,
            'message': message
        })