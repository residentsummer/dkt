#!/usr/bin/env python2

import os

from dkt.utils import *

from common import *
from core import register as register_action

def push(**options):
    name = options["name"]
    registry_tag = make_registry_tag(name, options)

    tagged = False
    try:
        docker("tag", name, registry_tag, **options)
        tagged = True

        docker("push", registry_tag, **options)
    finally:
        if tagged:
            docker("rmi", registry_tag, **options)

register_action("push", push, {"help": "Push image to the local registry"},
        [(["name"], {"help": "Name (with optional tag) of image to push",
                     "metavar": "NAME[:TAG]"})])

