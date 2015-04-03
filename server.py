from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import task

class TestFactory(WebSocketServerFactory):
    blah = 0

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.factory.blah += 1
        print self.factory.blah
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        task.LoopingCall(runEverySecond, self, "asdf").start(1/30.0)

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

def runEverySecond(connection, string):
    connection.sendMessage(string, False)

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor
    task.LoopingCall(runEverySecond)

    log.startLogging(sys.stdout)

    factory = TestFactory("ws://0.0.0.0:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()