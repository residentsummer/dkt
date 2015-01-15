#!/usr/bin/env python2

import os

from dkt.utils import *

from common import *
from core import register as register_action

def pull(**options):
    name = options["name"]
    registry_tag = make_registry_tag(name, options)

    pulled = False
    try:
        docker("pull", registry_tag, **options)
        pulled = True

        docker("tag", registry_tag, name, **options)
    finally:
        if pulled:
            docker("rmi", registry_tag, **options)

register_action("pull", pull, {"help": "Pull image from the local registry"},
        [(["name"], {"help": "Name (with optional tag) of image to pull",
                     "metavar": "NAME[:TAG]"})])

