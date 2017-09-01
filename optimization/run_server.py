from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import optimize
import json
import traceback

class SimpleEcho(WebSocket):
    recv = ""
    send = ""
    def optimize(self):
        if self.data == '{"type":"alive"}':
            pass
        try:
            web_output = optimize.handle_web_input(self.data)
            self.sendMessage(web_output)
        except:
            tb = traceback.format_exc()
            print('\n%s\n' % tb)
            self.sendMessage('{"error": "%s"}' % tb)

    def handleMessage(self):
        print(self.data)
        self.optimize()

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')



server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()
