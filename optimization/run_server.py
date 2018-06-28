# Copyright 2018 AdaM Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import logging
import optimize
import json
import traceback

logger = logging.getLogger('SoManyScreens_backend')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

port = 8080

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
            # logger.info(web_output)
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
