import json
import sys
from twisted.python import log
from twisted.internet import task
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from lanturn.game import Game

class Message(object):
    def __init__(self, message_json, player_id, connection):
        self.data = json.loads(message_json)
        self.player_id = player_id
        self.type = self.data['type']
        self.connection = connection

class Server(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.game = Game()
        self.message_handlers = self.game.get_message_handlers()
        task.LoopingCall(self.game.update, 1/2.0).start(1/2.0)

    def handle_message(self, message):  
        handler = self.message_handlers.get(message.type)
        if handler is None:
            print 'Could not find handler for type: <{}>'.format(message.type)
            return

        # print 'Handling message of type: <{}>'.format(message.type)
        return handler(message)

class MyServerProtocol(WebSocketServerProtocol):
    def __init__(self, *args, **kwargs):
        super(MyServerProtocol, self).__init__(*args, **kwargs)
        self.player_id = None

    def onConnect(self, request):
        print 'Client connecting: {0}'.format(request.peer)

    def onMessage(self, payload, isBinary):
        message = Message(
            payload.decode('utf8'),
            self.player_id,
            self
        )

        self.factory.handle_message(message)

    def onClose(self, wasClean, code, reason):
        print 'WebSocket connection closed: {}'.format(reason)

if __name__ == '__main__':
    # log.startLogging(sys.stdout)

    factory = Server('ws://0.0.0.0:9000', debug=False)
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()
