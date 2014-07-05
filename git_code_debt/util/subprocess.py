from __future__ import absolute_import

import subprocess


class CalledProcessError(RuntimeError):
    pass


def cmd_output(*cmd, **kwargs):
    encoding = kwargs.pop('encoding', 'UTF-8')

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

    if encoding is not None:
        stdout = stdout.decode(encoding)

    return stdout
