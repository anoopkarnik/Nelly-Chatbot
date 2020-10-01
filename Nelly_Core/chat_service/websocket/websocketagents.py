#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from chat_service.core.chatserviceagents import ChatServiceAgent


class WebsocketAgent(ChatServiceAgent):
    """
    Class for a person that can act in a ParlAI world via websockets.
    """

    def __init__(self, opt, manager, receiver_id, task_id):
        print("WebSocketAgent receiverID is : " + receiver_id)
        self.session_id = receiver_id
        super().__init__(opt, manager, receiver_id, task_id)
        self.message_partners = []
        self.action_id = 1


    def observe(self, act):
        """
        Send an agent a message through the websocket manager.

        Only attachments of type `image` are currently supported. In the case of
        images, the resultant message will have a `text` field which will be a
        base 64 encoded image and `mime_type` which will be an image mime type.

        Args:
            act: dict. If act contain an `payload` key, then a dict should be
                provided for the value in `payload`. Otherwise, act should be
                a dict with the key `text` for the message.
                For the `pyaload` dict, this agent expects a `type` key, which
                specifies whether or not the attachment is an image. If the
                attachment is an image, a `data` key must be specified with a
                base 64 encoded image.
                A `quick_replies` key can be provided with a list of string quick
                replies for any message
        """
        super(WebsocketAgent, self).observe(act)


    def put_data(self, message):
        """
        Put data into the message queue.

        Args:
            message: dict. An incoming websocket message. See the chat_services
                README for the message structure.
        """
        logging.info(f"Received new message: {message}")
        action = {
            'episode_done': False,
            'text': message.get('text', ''),
            'payload': message.get('payload'),
        }

        self._queue_action(action, self.action_id)
        self.action_id += 1

    def send_data(self, message):
        quick_replies = message.get('quick_replies', None)
        if message.get('payload', None):
            self.manager.observe_payload(self.id, message['payload'], quick_replies)
        else:
            self.manager.observe_message(self.id, message['text'], quick_replies)