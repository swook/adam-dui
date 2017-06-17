from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

class SimpleEcho(WebSocket):
    recv = ""
    send = ""
    def optimize(self):
        print('optimizing called')
        self.recv = json.loads(self.data)
        print(self.recv)
        self.send = json.dumps(self.recv, sort_keys=False,indent=4,separators=(',', ':'))

        self.sendMessage(self.send)

    def handleMessage(self):
        print(self.data)
        self.optimize()
		
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


		
server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()