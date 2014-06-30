from __future__ import absolute_import

import subprocess


class CalledProcessError(RuntimeError):
    pass


def cmd_output(*cmd, **kwargs):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs
    )
    stdout, stderr = proc.communicate()
    retcode = proc.returncode

    if retcode:
        raise CalledProcessError(cmd, stdout, stderr)

    return stdout
