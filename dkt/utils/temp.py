#!/usr/bin/env python2

import os
import time
import shutil
import inspect
import tempfile
import functools

from path import Path

def with_temp_dir(temp_dir_kw):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                if ( temp_dir_kw in kwargs and
                     kwargs[temp_dir_kw] is not None ):
                    clean = False

                    # Convert regular string path to Path class
                    if not isinstance(kwargs[temp_dir_kw], Path):
                        kwargs[temp_dir_kw] = Path.normalize(kwargs[temp_dir_kw])
                else:
                    clean = True
                    temp_dir = tempfile.mkdtemp()
                    kwargs[temp_dir_kw] = Path(temp_dir)

                return f(*args, **kwargs)
            finally:
                # Clean temp stuff
                if clean:
                    shutil.rmtree(temp_dir)

        return wrapper
    return decorator

def fmkdtemp(work_dir, skip_mkdir=False):
    timestamp = int(time.time() * 1000000)
    # Will be used for dir_name generation
    caller_frame = inspect.currentframe().f_back

    dir_name = "%d.%s.%s" % (
            timestamp,
            caller_frame.f_globals['__name__'],
            caller_frame.f_code.co_name)
    # Not sure if work_dir needs normalization
    path = Path(work_dir, dir_name)

    # Create temp dir and return a path
    if not skip_mkdir:
        os.mkdir(path)

    return path

