from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import os


@contextlib.contextmanager
def cwd(path):
    original_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)
