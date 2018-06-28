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
"""Websocket server for handling messages and passing to optimizer."""
from websocket_server import WebsocketServer
import logging
import optimize
import json
import traceback

logger = logging.getLogger('SoManyScreens_backend')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def handle_message(client, server, message):
    """Handle message from client."""
    # Handle keep-alive
    try:
        json_request = json.loads(message)
    except:
        pass
    if 'type' in json_request and json_request['type'] == 'alive':
        return

    # Handle proper input
    try:
        web_output = optimize.handle_web_input(message)
        # logger.info(web_output)
        server.send_message(client, web_output)
    except:
        tb = traceback.format_exc()
        logger.debug('\n%s\n' % tb)
        server.send_message(client, json.dumps({
            'error': tb,
            'token': json_request['token'],
        }).decode('utf-8'))

port = 8001
logger.info('Starting backend at port %d' % port)
server = WebsocketServer(port, host='0.0.0.0')  # , loglevel=logging.INFO)
server.set_fn_new_client(
    lambda client, server:
        logger.info('%s:%d connected.' % client['address'])
)
server.set_fn_client_left(
    lambda client, server:
        logger.info('%s:%d disconnected.' % client['address'])
)
server.set_fn_message_received(handle_message)
server.run_forever()
