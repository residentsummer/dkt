#!/usr/bin/env python2

import os

class Path(unicode):
    '''
    Helper class for easy creation of sub-paths.

    No FS manipulations are done, only strings concatenation!

    E.g.:
        try:
            tmp = Path(tempfile.mkdtemp())
            data_dir = tmp("template")
            config = tmp("config.json")

            shutil.copytree(src, data_dir)
            download(url, config)
            do_stuff(config, data_dir)
            upload(data_dir("results", "out.json"), url)
        finally:
            shutil.rmtree(tmp)
    '''

    def __new__(cls, *bases):
        return unicode.__new__(cls, os.path.join(*bases))

    def __call__(self, *xs):
        return Path(self, *xs)

    @classmethod
    def normalize(cls, x, cwd=None):
        '''
        Parse a Path out of string.
            - Aware of ~ and env vars
            - Returns normalized, absolute path
            - Optional toplevel (CWD) may be provided
        '''
        # Expand ~ and env
        x = os.path.expandvars(os.path.expanduser(x))

        # Treat relative paths
        if not os.path.isabs(x):
            cwd = os.path.normpath(cwd or os.curdir)
            x = os.path.join(cwd, x)

        # Return absolute Path
        return cls(os.path.abspath(x))

