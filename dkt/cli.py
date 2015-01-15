#!/usr/bin/env python2

import os
import configargparse

import actions

from dkt.utils import *
from dkt.utils import Path

def main():
    parser = configargparse.ArgumentParser(description="Docker tool - simplify images building and \
            submitting to local registry.\n\n")
    parser.add_argument("-H", help="Socket or host/port where docker daemon runs",
            dest="DOCKER_HOST", env_var="DOCKER_HOST")
    parser.add_argument("-R", help="Host and port where local registry is located. \
            Will be guessed from DOCKER_HOST if not specified.",
            dest="DKT_REGISTRY_HOST", env_var="DKT_REGISTRY_HOST")
    parser.add_argument("-u", help="Username in local registry",
            dest="DKT_REGISTRY_USERNAME", env_var="DKT_REGISTRY_USERNAME")
    parser.add_argument("-N", help="Prefix for images in registry (e.g. \
            localhost:5000/<prefix>/<name>). Will be guessed from \
            DKT_REGISTRY_USERNAME if not specified.",
            dest="DKT_REGISTRY_PREFIX", env_var="DKT_REGISTRY_PREFIX")
    parser.add_argument("-v", help="Verbosity (also try -vv and more)",
            dest="verbosity", action='count', default=0)

    # This will extend parser to know each action
    actions.bind(parser)

    # Parse args - unknown ones will be passed directly to docker
    args, other_args = parser.parse_known_args()
    args.other_args = other_args
    actions.perform(args)

