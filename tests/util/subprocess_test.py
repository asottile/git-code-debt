# -*- coding: UTF-8 -*-
# pylint:disable=star-args
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import six

from git_code_debt.util.subprocess import CalledProcessError
from git_code_debt.util.subprocess import cmd_output


def test_subprocess_encoding():
    # Defaults to utf-8
    ret = cmd_output('echo', '☃'.encode('UTF-8'))
    assert type(ret) is six.text_type
    assert ret == '☃\n'


def test_no_encoding_gives_bytes():
    ret = cmd_output('echo', '☃'.encode('UTF-8'), encoding=None)
    assert type(ret) is bytes
    assert ret == '☃\n'.encode('UTF-8')


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
