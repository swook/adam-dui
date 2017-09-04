from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import logging
import optimize
import json
import traceback

logger = logging.getLogger('SoManyScreens_backend')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class SimpleEcho(WebSocket):

    def optimize(self):
        # Handle keep-alive
        try:
            json_request = json.loads(self.data)
        except:
            pass
        if 'type' in json_request and json_request['type'] == 'alive':
            return

        # Handle proper input
        try:
            web_output = optimize.handle_web_input(self.data)
            self.sendMessage(web_output)
        except:
            tb = traceback.format_exc()
            logger.debug('\n%s\n' % tb)
            self.sendMessage(json.dumps({
                'error': tb,
                'token': json_request['token'],
            }).decode('utf-8'))

    def handleMessage(self):
        # logger.debug('\nReceived data from client:\n%s\n' % self.data)
        self.optimize()

    def handleConnected(self):
        logger.info('%s:%d connected.' % self.address)

    def handleClose(self):
        logger.info('%s:%d disconnected.' % self.address)


port = 8001
logger.info('Starting backend at port %d' % port)
server = SimpleWebSocketServer('', port, SimpleEcho)
server.serveforever()
