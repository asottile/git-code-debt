from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.server.app import main


def test_file_does_not_exist():
    assert main(argv=['i_dont_exist.db']) == 1
