#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Script for safety protected interaction between a local human keyboard input and a
trained model.
"""

import random

from core.safe_local_human.safe_local_human import SafeLocalHumanAgent
from core.agents import create_agent
from core.params import ParlaiParser
from core.worlds import create_task


def setup_bst(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True, 'Interactive chat with a model')
    parser.add_argument('-d', '--display-examples', type='bool', default=False)
    parser.add_argument(
        '--display-prettify',
        type='bool',
        default=False,
        help='Set to use a prettytable when displaying '
        'examples with text candidates',
    )
    parser.add_argument(
        '--display-ignore-fields',
        type=str,
        default='label_candidates,text_candidates',
        help='Do not display these fields',
    )
    parser.add_argument(
        '-it',
        '--interactive-task',
        type='bool',
        default=True,
        help='Create interactive version of task',
    )
    parser.set_defaults(interactive_mode=True, task='interactive')
    SafeLocalHumanAgent.add_cmdline_args(parser)
    return parser


def start_bst(opt=None, print_parser=None, withparley=False):
    if print_parser is not None:
        if print_parser is True and isinstance(opt, ParlaiParser):
            print_parser = opt
        elif print_parser is False:
            print_parser = None
    if isinstance(opt, ParlaiParser):
        print('[ Deprecated Warning: interactive should be passed opt not Parser ]')
        opt = opt.parse_args()

    # Create model and assign it to the specified task
    agent = create_agent(opt, requireModelExists=True)
    if print_parser:
        # Show arguments after loading model
        print_parser.opt = agent.opt
        print_parser.print_args()
    human_agent = SafeLocalHumanAgent(opt)
    world = create_task(opt, [human_agent, agent])

    # Interact until episode done
    if withparley is True:
        while True:
            world.parley()
            bot_act = world.get_acts()[-1]
            if 'bot_offensive' in bot_act and bot_act['bot_offensive']:
                agent.reset()

            if opt.get('display_examples'):
                print('---')
                print(world.display())
            if world.epoch_done():
                print('EPOCH DONE')
                break
    else:
        print("task and world setup is complete")
        return world



if __name__ == '__main__':
    random.seed(42)
    parser = setup_bst()
    start_bst(parser.parse_args(print_args=True), print_parser=parser, withparley=True)
