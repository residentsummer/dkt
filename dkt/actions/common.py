#!/usr/bin/env python2

import os
import re

from dkt.utils import *

docker_env_vars = ["DOCKER_HOST"]
popen_kwargs = ["cwd", "env", "stdin", "stdout", "stderr"]

# MAKE A DOCKER_COMMANDER CLASS
def docker(*in_args, **in_kwargs):
    args = ["docker"]
    args.extend(in_args)

    # Select popen keyword args from in_kwargs
    run_kwargs = {k:v
            for k, v in in_kwargs.iteritems()
            if k in popen_kwargs}

    # Push cmd options to the environment
    env = (("env" in run_kwargs) and run_kwargs["env"]) or os.environ
    env = env.copy() # Oh, this crazy mutable world...
    for v in docker_env_vars:
        if in_kwargs[v]:
            env[v] = in_kwargs[v]
    run_kwargs["env"] = env

    return run(args, **run_kwargs)

def guess_registry_host(options):
    docker_host = options["DOCKER_HOST"]
    registry_host = options["DKT_REGISTRY_HOST"]

    if not registry_host:
        # This re is too permissive
        tcp_pattern = r'tcp://([^:]+):\d+$'
        if docker_host and re.match(tcp_pattern, docker_host):
            registry_host = re.sub(tcp_pattern, r'http://\1:5000', docker_host)
        else:
            registry_host = "localhost:5000"

        if options["verbosity"] > 0:
            print "Guessed registry host to be %s" % registry_host

    if not registry_host:
        print "You should specify registry host!"
        raise ValueError("Registry host is not specified")

    return registry_host

def strip_registry_host_proto(registry_host):
    return re.sub(r'^.*://', r'', registry_host)

def guess_registry_prefix(options):
    registry_username = options["DKT_REGISTRY_USERNAME"]
    registry_prefix = options["DKT_REGISTRY_PREFIX"]

    if not registry_prefix and registry_username:
        registry_prefix = registry_username

        if options["verbosity"] > 0:
            print "Guessed registry prefix to be %s" % registry_prefix

    if not registry_prefix:
        print "You should specify registry prefix!"
        raise ValueError("Registry prefix is not specified")

    return registry_prefix

def make_registry_tag(name, options):
    registry_host = guess_registry_host(options)
    registry_prefix = guess_registry_prefix(options)

    # Prepare tag for pushing image
    registry_tag = "%s/%s/%s" % (strip_registry_host_proto(registry_host),
            registry_prefix, name)

    return registry_tag

def registry_login(**options):
    registry_host = guess_registry_host(options)
    args = ["login"]

    if options["DKT_REGISTRY_USERNAME"]:
        args += ["--username", options["DKT_REGISTRY_USERNAME"]]

    args.append(registry_host)
    docker(*args, **options)

