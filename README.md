# dkt
A tiny helper tool for Docker

    usage: dkt [-h] [-H DOCKER_HOST] [-R DKT_REGISTRY_HOST]
               [-u DKT_REGISTRY_USERNAME] [-N DKT_REGISTRY_PREFIX] [-v]
               {bootstrap,login,build,sweep,push,pull,rls} ...

    Docker tool - simplify images building and submitting to local registry. If an
    arg is specified in more than one place, then command-line values override
    environment variables which override defaults.

    positional arguments: {bootstrap,login,build,sweep,push,pull,rls}
        bootstrap           Prepare local docker registry
        login               Login into docker registry
        build               Build an image from Dockerfile (and dkt files)
        sweep               Remove exited containers and dangling images.
                            !!!ACHTUNG!!! It will remove data-containers as well!
                            Not the actual volumes, though.
        push                Push image to the local registry
        pull                Pull image from the local registry
        rls                 List repositories in registry

    optional arguments:
        -h, --help            show this help message and exit
        -H DOCKER_HOST        Socket or host/port where docker daemon runs [env var:
                              DOCKER_HOST]
        -R DKT_REGISTRY_HOST  Host and port where local registry is located. Will be
                              guessed from DOCKER_HOST if not specified. [env var:
                              DKT_REGISTRY_HOST]
        -u DKT_REGISTRY_USERNAME
                              Username in local registry [env var:
                              DKT_REGISTRY_USERNAME]
        -N DKT_REGISTRY_PREFIX
                              Prefix for images in registry (e.g.
                              localhost:5000/<prefix>/<name>). Will be guessed from
                              DKT_REGISTRY_USERNAME if not specified. [env var:
                              DKT_REGISTRY_PREFIX]
        -v                    Verbosity (also try -vv and more)
