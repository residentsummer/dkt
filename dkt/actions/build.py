#!/usr/bin/env python2

import os

from dkt.utils import *

from common import docker
from core import register as register_action

@shared_work_dir
def build(**options):
    wd = fmkdtemp(options["work_dir"])

    # Check if valid dir is specified as 'path'
    tpl_path = options["path"]
    if not os.path.exists(tpl_path("Dockerfile")):
        raise ValueError("No Dockerfile found in %s/" % tpl_path)

    # Prepare build dir
    build_path = wd("build")
    options["cwd"] = build_path
    shutil.copytree(tpl_path, build_path)

    # Determine image name:tag
    if options["tag"]:
        image_name = options["tag"]
    else:
        image_name = os.path.basename(tpl_path)

        if options["verbosity"] > 0:
            print "Guessed image tag to be \"%s\"" % image_name

    # Invoke docker build and pre/post scripts
    try:
        if os.path.exists(build_path("pre.dkt")):
            print "Step dkt.pre"
            run(["./pre.dkt"], cwd=build_path)

        build_args = ["build", "-t", image_name]
        build_args.extend(options["other_args"])

        if options["verbosity"] == 0:
            build_args.append("-q")
        build_args.append(build_path)

        # print build_args, options
        docker(*build_args, **options)

        if os.path.exists(build_path("post.dkt")):
            print "Step dkt.post"
            run(["./post.dkt", image_name], cwd=build_path)
    except:
        print "Image build failed!"
        raise

register_action("build", build, {"help": "Build an image from Dockerfile (and dkt files)"},
        [(["path"], {"help": "Path to a dir with the Dockerfile", "type": Path.normalize}),
         (["-t", "--tag"], {"help": "Repository name (and optionally a tag) to be applied to the resulting image in case of success",
                            "metavar": "NAME[:TAG]", "dest": "tag"})])

