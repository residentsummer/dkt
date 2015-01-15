#!/usr/bin/env python2

from subprocess import Popen, CalledProcessError

def run(*args, **kwargs):
    proc = Popen(*args, **kwargs)
    pipes = proc.communicate()

    if proc.returncode != 0:
        rc = proc.returncode
        cmd = " ".join(*args)
        raise CalledProcessError(rc, cmd)

    return pipes

