from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import optimize
import json

port = 8080

class SimpleEcho(WebSocket):
    recv = ""
    send = ""
    def optimize(self):
        try:
            web_output = optimize.handle_web_input(self.data)
            self.sendMessage(web_output)
        except Exception as e:
            print(e)
            pass

    def handleMessage(self):
        print(self.data)
        self.optimize()

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')



server = SimpleWebSocketServer('', port, SimpleEcho)
print 'server running on port', port
server.serveforever()
