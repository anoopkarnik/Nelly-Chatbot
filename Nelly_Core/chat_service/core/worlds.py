#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# py parlai/chat_service/tasks/overworld_demo/run.py --debug --verbose

from core.worlds import World
from chat_service.core.onboardworld import OnboardWorld
from core.agents import create_agent_from_shared


# ---------- Chatbot demo ---------- #
from utils import logging


class MessengerBotChatOnboardWorld(OnboardWorld):
    """
    Example messenger onboarding world for Chatbot Model.
    """

    @staticmethod
    def generate_world(opt, agents):
        return MessengerBotChatOnboardWorld(opt=opt, agent=agents[0])

    def parley(self):
        self.episodeDone = True


class MessengerBotChatTaskWorld(World):
    """
    Example one person world that talks to a provided agent (bot).
    """

    MAX_AGENTS = 1
    MODEL_KEY = 'blender_90M'

    def __init__(self, opt, agent):
        self.agent = agent
        self.episodeDone = False
        #self.model = bot
        self.first_time = True

    @staticmethod
    def generate_world(opt, agents):
        if opt['model'] is None:
            raise RuntimeError("Model must be specified")

        # the notes suggest using BST world or HogwildWorld
        # needs review
        return MessengerBotChatTaskWorld(
            opt,
            agents[0],
        )

    @staticmethod
    def assign_roles(agents):
        agents[0].disp_id = 'ChatbotAgent'

    def parley(self):
        if self.first_time:
            """self.agent.observe(
                {
                    'id': 'World',
                    'text': 'Welcome to the ParlAI Chatbot demo. '
                    'You are now paired with a bot - feel free to send a message.'
                    'Type [DONE] to finish the chat.',
                }
            )"""
            # Need to load persona here.
            self.first_time = False
        a = self.agent.get_new_act_message()
        if a is not None:
            if '[DONE]' in a['text']:
                self.episodeDone = True
                return None
            else:
                self.agent.observe(a)
                response = self.agent.act()
                logging.info("Reponding to id: " + response[0]['id']+ " \n with : " + response[0]['text'])
                if response is not  None:
                    self.agent.observe(response[0])
                    self.agent.send_data(response[0])

    def episode_done(self):
        return self.episodeDone

    def shutdown(self):
        self.agent.shutdown()


# ---------- Overworld -------- #
class MessengerOverworld(World):
    """
    World to handle moving agents to their proper places.
    """

    def __init__(self, opt, agent):
        self.agent = agent
        self.opt = opt
        self.first_time = True
        self.episodeDone = False

    @staticmethod
    def generate_world(opt, agents):
        return MessengerOverworld(opt, agents[0])

    @staticmethod
    def assign_roles(agents):
        for a in agents:
            a.disp_id = 'Agent'

    def episode_done(self):
        return self.episodeDone

    def parley(self):
        if self.first_time:
            self.agent.observe(
                {
                    'id': 'Overworld',
                    'text': 'Welcome to the overworld for the ParlAI messenger '
                    'chatbot demo. Please type "begin" to start.',
                    'quick_replies': ['begin'],
                }
            )
            self.first_time = False
        a = self.agent.act()
        if a is not None and a['text'].lower() == 'begin':
            self.episodeDone = True
            return 'default'
        elif a is not None:
            self.agent.observe(
                {
                    'id': 'Overworld',
                    'text': 'Invalid option. Please type "begin".',
                    'quick_replies': ['begin'],
                }
            )
