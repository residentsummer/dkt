#!/usr/bin/env python2

parser_actions = []
action_functions = {}

def register(choice, fn, kwargs=None, action_arguments=None):
    global parser_actions
    global action_functions

    action_functions[choice] = fn
    parser_actions.append((choice, (kwargs or {}), (action_arguments or [])))

def bind(parser):
    subparsers = parser.add_subparsers(dest="action")

    for choice, kwargs, action_arguments in parser_actions:
        subparser = subparsers.add_parser(choice, **kwargs)
        for args, kwargs in action_arguments:
            subparser.add_argument(*args, **kwargs)

def perform(args):
    args_dict = vars(args)
    action = args_dict.pop("action")

    action_functions[action](**args_dict)

