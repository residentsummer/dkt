#!/usr/bin/env python2

import requests

from common import *
from core import register as register_action

#TODO Produce output, similar to `docker images`
def rls(**options):
    registry_host = guess_registry_host(options)
    registry_prefix = guess_registry_prefix(options)

    resp = requests.get(registry_host + "/v1/search",
            params={"q": registry_prefix + "/"})
    images = resp.json["results"]

    for image in images:
        print re.sub(r'^%s\/' % registry_prefix, r'', image["name"])

register_action("rls", rls, {"help": "List repositories in registry"})

