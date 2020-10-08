#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import requests
import logging
import uuid
from typing import Dict, TypeVar
from config import Config

from tornado.websocket import WebSocketHandler

def get_rand_id():
    return str(uuid.uuid4())


T = TypeVar('T', bound='MessageSocketHandler')

class SessionID:
    sid = str('wrong sid')


class MessageSocketHandler(WebSocketHandler):
    def __init__(self: T, *args, **kwargs):
        
        self.subs: Dict[int, T] = kwargs.pop('subs')
        def _default_callback(message, socketID):
            logging.warn(f"No callback defined for new WebSocket messages.")
        logging.info("starting message socket handler")
        self.message_callback = kwargs.pop('message_callback', _default_callback)
        super().__init__(*args, **kwargs)
        self.sid = None
        
    def open(self):
        """
        Opens a websocket and assigns a random UUID that is stored in the class-level
        `subs` variable.
        """
        server = Config.Server
        port = 8080
        headers = (self.request.headers).get("Authorization")
        sid = headers.partition(' ')[2]
        self.sid = sid
        response_text = requests.get('http://{}:{}/validate_sessionId'.format(server,port),headers={'session_id':sid})
        if response_text.status_code == 200:
            self.sid = response_text.json()["data"]["session_id"]
            if self.sid not in self.subs.values():
                self.subs[self.sid] = self    
                self.set_nodelay(True)
                logging.info(f"Opened new socket from ip: {self.request.remote_ip}")
                logging.info(f"Current subscribers: {self.subs}")
        else:
            #logging.error("Cannot Verify Session ID")
            self.sid = sid
            if self.sid not in self.subs.values():
                self.subs[self.sid] = self    
                self.set_nodelay(True)
                logging.info(f"Opened new socket from ip: {self.request.remote_ip}")
                logging.info(f"Current subscribers: {self.subs}")
        

    def on_close(self):
        """
        Runs when a socket is closed.
        """
        logging.info(f"Closing the Agent: {self.sid}")
        del self.subs[self.sid]

    def on_message(self, message_text):
        """
        Callback that runs when a new message is received from a client See the
        chat_service README for the resultant message structure.
        Args:
            message_text: A stringified JSON object with a text or attachment key.
                `text` should contain a string message and `attachment` is a dict.
                See `WebsocketAgent.put_data` for more information about the
                attachment dict structure.
        """
        logging.info('websocket message from client: {}'.format(message_text))
        message = json.loads(message_text)
        if self.sid is not None:
            message = {
                'text': message.get('text', ''),
                'payload': message.get('payload'),
                'sender': {'id': self.sid},
                'recipient': {'id': 0},
            }
            self.message_callback(message)
        else:
            logging.error("No response from Nelly as the session ID is invalid")

    def check_origin(self, origin):
        return True
