#!/usr/bin/env python2

import os
from subprocess import PIPE

from dkt.utils import *

from common import *
from core import register as register_action

def sweep(**options):
    output, _ = docker("ps",
            "-a", # Show all containers (incl. stopped)
            "-q", # Only output ids
            "-f", "status=exited", # f means filter
            stdout=PIPE, # We'll read a list of container IDs
            **options)
    containers = filter(None, output.strip().split("\n"))

    # Remove containers to free images
    if len(containers):
        docker("rm", *containers, **options)

    output, _ = docker("images",
            "-a", # Show all images (incl. not tagged)
            "-q", # Only output ids
            "-f", "dangling=true", # f means filter
            stdout=PIPE, # We'll read a list of container IDs
            **options)
    images = filter(None, output.strip().split("\n"))

    if len(images):
        docker("rmi", *images, **options)

register_action("sweep", sweep, {"help": "Remove exited containers and dangling images. \
        !!!ACHTUNG!!! It will remove data-containers as well! \
        Not the actual volumes, though."})

