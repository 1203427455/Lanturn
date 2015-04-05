from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print('Server connected: {0}'.format(response.peer))

    def onOpen(self):
        print('WebSocket connection open.')
        for i in range(1):
            self.sendMessage(json.dumps({
                'type': 'connect',
                'username': str(i)
            }))

        def hello(offset=0):
            self.sendMessage(json.dumps({
                'type': 'move',
                'position': (offset, 0)
            }))
            self.factory.reactor.callLater(1, hello, offset+1)

        hello()

    def onMessage(self, payload, isBinary):
           print('Text message received: {0}'.format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {0}'.format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory('ws://localhost:9000', debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP('192.168.1.10', 9000, factory)
    reactor.run()