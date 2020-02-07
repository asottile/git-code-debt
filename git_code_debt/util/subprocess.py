import subprocess
from typing import Any


class CalledProcessError(RuntimeError):
    pass


def cmd_output_b(*cmd: str, **kwargs: Any) -> bytes:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs,
    )
    stdout, stderr = proc.communicate()

    if proc.returncode:
        raise CalledProcessError(cmd, proc.returncode, stdout, stderr)

    return stdout


def cmd_output(*cmd: str, **kwargs: Any) -> str:
    return cmd_output_b(*cmd, **kwargs).decode()
