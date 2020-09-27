#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from random import random
import requests

import websocket
from chat_service.client.interactive_web import WEB_HTML, STYLE_SHEET, FONT_AWESOME

SHARED = {}
SHARED['websockets'] = {}
SESSION_CTR = {}
SESSION_CTR['id'] = 0

new_message = None
message_available = threading.Event()


class BrowserHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, reply_text, sessionid):
        data = {}
        data['text'] = reply_text.decode('utf-8')
        if data['text'] == "[DONE]":
            print('[ Closing socket... ]')
            SHARED['websockets'].__getitem__(sessionid).close()
            SHARED['wb'].shutdown()
        json_data = json.dumps(data)
        SHARED['websockets'].get(sessionid).send(json_data)

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self._interactive_running(body, self.get_sessionid())
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            model_response = {'id': 'Nelly', 'episode_done': False}
            message_available.wait()
            model_response['text'] = new_message
            message_available.clear()
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def get_sessionid(self):
        complete_cookie = self.headers['Cookie']
        strings = {}
        for str in complete_cookie.split('; '):
            temp = str.split('=')
            if len(temp) == 2:
                strings.update({temp[0]: temp[1]})
        return strings['sessionid']

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path is '/':
            ws = open_new_conn()
            current_session_id = SESSION_CTR["id"]
            new_session_id = current_session_id + 1
            SHARED['websockets'].update({str(new_session_id): ws})
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        cookie = cookies.SimpleCookie()
        if self.path is '/':
            current_session_id = SESSION_CTR["id"]
            new_session_id = current_session_id + 1
            SESSION_CTR["id"] = new_session_id
            cookie['sessionid'] = new_session_id
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        for morsel in cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())
        self.end_headers()
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)

def open_new_conn():
    port = 34596
    print("Connecting to port: ", port)
    ws = websocket.WebSocketApp(
        "ws://localhost:{}/websocket".format(port),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_ping=None,
        on_pong=None,
        keep_running=True,
    )
    print("Connection initialized" + ws.__str__())
    wst = threading.Thread(target=ws.run_forever, kwargs={'ping_interval': 5, 'ping_timeout': 2})
    wst.daemon = True
    wst.start()
    return ws



def on_message(ws, message):
    """
    Prints the incoming message from the server.

    :param ws: a WebSocketApp
    :param message: json with 'text' field to be printed
    """
    incoming_message = json.loads(message)
    global new_message
    new_message = incoming_message['text']
    message_available.set()
    print("Received:" + message)

def on_error(ws, error):
    """
    Prints an error, if occurs.

    :param ws: WebSocketApp
    :param error: An error
    """
    print(error)


def on_close(ws):
    """
    Cleanup before closing connection.

    :param ws: WebSocketApp
    """
    # Reset color formatting if necessary
    print("Connection closed on "+ ws.__str__())
    ws = SHARED['websockets'].pop(ws.get_mask_key)
    httpd = SHARED['wb']
    httpd.shutdown()


def _run_browser():
    host = 'localhost'
    serving_port = 8080

    httpd = HTTPServer((host, serving_port), BrowserHandler)

    print('Please connect to the link: http://{}:{}/'.format(host, serving_port))

    SHARED['wb'] = httpd

    httpd.serve_forever()


def on_open(ws):
    """
    Starts a new thread that loops, taking user input and sending it to the websocket.

    :param ws: websocket.WebSocketApp that sends messages to a browser_manager
    """
    print("Connection opened "+ws.__str__())




if __name__ == "__main__":
    threading.Thread(target=_run_browser).start()
