from __future__ import annotations

import pytest

from git_code_debt.util.subprocess import CalledProcessError
from git_code_debt.util.subprocess import cmd_output
from git_code_debt.util.subprocess import cmd_output_b


def test_subprocess_encoding():
    # Defaults to utf-8
    ret = cmd_output('echo', '☃')
    assert type(ret) is str
    assert ret == '☃\n'


def test_no_encoding_gives_bytes():
    ret = cmd_output_b('echo', '☃')
    assert ret == '☃\n'.encode()


def test_raises_on_nonzero():
    cmd = ('sh', '-c', 'echo "stderr" >&2 && echo "stdout" && exit 1')
    with pytest.raises(CalledProcessError) as exc_info:
        cmd_output(*cmd)

    assert exc_info.value.args == (
        cmd,
        1,
        b'stdout\n',
        b'stderr\n',
    )
