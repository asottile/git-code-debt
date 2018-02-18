from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.server.app import create_metric_config_if_not_exists
from git_code_debt.server.app import main


def test_file_does_not_exist():
    assert main(argv=['i_dont_exist.db']) == 1


def test_create_metric_config_if_not_exists_existing(tmpdir):
    metric_config = tmpdir.join('metric_config.yaml')
    with tmpdir.as_cwd():
        metric_config.write('Groups: []\nColorOverrides: []\n')

        create_metric_config_if_not_exists()

        after_contents = metric_config.read()
        assert after_contents == 'Groups: []\nColorOverrides: []\n'


def test_create_metric_config_if_not_exists_not_existing(tmpdir):
    with tmpdir.as_cwd():
        create_metric_config_if_not_exists()
    assert tmpdir.join('metric_config.yaml').exists()
