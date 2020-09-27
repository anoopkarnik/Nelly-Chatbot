#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Websocket Runner.
"""
from core.params import ParlaiParser
from chat_service.websocket.websocket_manager import WebsocketManager
import os
from core.opt import Opt as options
import sys as _sys
from core.Start_BST import setup_bst, start_bst

SERVICE_NAME = 'websocket'


def setup_args():
    """
    Set up args.
    """
    parser = ParlaiParser(False, False)
    parser.add_parlai_data_path()
    parser.add_websockets_args()
    return parser.parse_args()


def run(opt):
    """
    Run MessengerManager.
    """
    opt['service'] = SERVICE_NAME
    manager = WebsocketManager(opt)
    try:
        manager.start_task()
    except BaseException:
        raise
    finally:
        manager.shutdown()


def get_model_path(model_path):
    os.chdir('../')
    os.chdir('../')
    new_path = os.path.join(os.getcwd(), 'data')
    os.chdir(new_path)
    os.chdir(os.path.join(new_path, model_path))
    model_obs_path = os.getcwd()
    return model_obs_path


if __name__ == '__main__':
    """ parser = setup_bst()
    opt = parser.parse_args(print_args=True, print_parser=parser, withparley=False)
    import core.agents as agents
    opt = agents.create_agent_from_opt_file()"""

    opt_file = os.path.abspath(os.path.join(os.getcwd(), '../..')) + \
               '/data/models' + '/' + _sys.argv[1:][0] + '.opt'
    if os.path.exists(opt_file):
        if os.path.isfile(opt_file):
            opt = options.load(opt_file)
            run(opt)
