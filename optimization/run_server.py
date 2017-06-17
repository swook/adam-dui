from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import optimize
import json

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



server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()
