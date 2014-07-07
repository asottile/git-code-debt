from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path

from git_code_debt.server.app import create_metric_config_if_not_exists
from git_code_debt.server.app import main
from testing.utilities.cwd import cwd


def test_file_does_not_exist():
    assert main(argv=['i_dont_exist.db']) == 1


def test_create_metric_config_if_not_exists_existing(tmpdir):
    with cwd(tmpdir.strpath):
        with io.open(
            'metric_config.yaml', 'w',
        ) as metric_config_file:  # pragma: no cover (PY26 derps on `with`)
            metric_config_file.write('Groups: []\nColorOverrides: []\n')

        create_metric_config_if_not_exists()

        after_contents = io.open('metric_config.yaml').read()
        assert after_contents == 'Groups: []\nColorOverrides: []\n'


def test_create_metric_config_if_not_exists_not_existing(tmpdir):
    with cwd(tmpdir.strpath):
        create_metric_config_if_not_exists()

        assert os.path.exists('metric_config.yaml')
