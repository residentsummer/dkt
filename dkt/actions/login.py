#!/usr/bin/env python2

from common import registry_login
from core import register as register_action

def login(**options):
    registry_login(**options)

register_action("login", login, {"help": "Login into docker registry"})

