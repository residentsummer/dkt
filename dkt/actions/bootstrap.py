#!/usr/bin/env python2

from common import docker, registry_login
from core import register as register_action

def bootstrap(**options):
    print "Bootstraping local registry for docker"

    docker("pull", "registry:latest", **options)
    docker("run",
            "-d", # daemonize
            "-e", "GUNICORN_OPTS=[--preload]", # push env var
            "-p", "5000:5000", # export registry port
            "--name", "registry", # assign name to container
            "registry:latest", **options)
    registry_login(**options)

register_action("bootstrap", bootstrap, {"help": "Prepare local docker registry"})

