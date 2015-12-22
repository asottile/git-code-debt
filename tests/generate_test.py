from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import io
import os
import os.path

import pytest
import yaml

from git_code_debt.generate import get_options_from_argparse
from git_code_debt.generate import get_options_from_config
from git_code_debt.generate import increment_metric_values
from git_code_debt.generate import main
from git_code_debt.generate_config import GenerateOptions
from git_code_debt.metric import Metric
from git_code_debt.util.subprocess import cmd_output
from testing.utilities.cwd import cwd


def test_increment_metrics_first_time():
    metrics = collections.defaultdict(int)
    increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
    assert metrics == {'foo': 1, 'bar': 2}


def test_increment_metrics_already_there():
    metrics = collections.defaultdict(int, {'foo': 2, 'bar': 3})
    increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
    assert metrics == {'foo': 3, 'bar': 5}


def test_generate_integration(sandbox, cloneable):
    main([cloneable, sandbox.db_path])


def test_generate_integration_config_file(sandbox, cloneable, tempdir_factory):
    tmpdir = tempdir_factory.get()
    config_filename = os.path.join(tmpdir, 'generate_config.yaml')
    with io.open(config_filename, 'w') as config_file:
        yaml.dump(
            {'repo': cloneable, 'database': sandbox.db_path},
            stream=config_file,
        )
    with cwd(tmpdir):
        main([])


def test_main_no_files_exist(cloneable):
    ret = main([cloneable, 'i_dont_exist.db'])
    assert ret == 1


def get_metric_data_count(sandbox):
    with sandbox.db() as db:
        return db.execute('SELECT COUNT(*) FROM metric_data').fetchone()[0]


def test_generate_integration_previous_data(sandbox, cloneable):
    main([cloneable, sandbox.db_path])
    before_data_count = get_metric_data_count(sandbox)
    assert before_data_count > 0
    main([cloneable, sandbox.db_path])
    after_data_count = get_metric_data_count(sandbox)
    assert before_data_count == after_data_count


def test_generate_new_data_created(sandbox, cloneable):
    main([cloneable, sandbox.db_path])
    before_data_count = get_metric_data_count(sandbox)
    # Add some commits
    with cwd(cloneable):
        cmd_output('git', 'commit', '--allow-empty', '-m', 'bar')
    main([cloneable, sandbox.db_path])
    after_data_count = get_metric_data_count(sandbox)
    assert after_data_count > before_data_count


def test_regression_for_issue_10(sandbox, cloneable):
    # Create a commit, then create another commit at a previous time
    with cwd(cloneable):
        cmd_output(
            'git', 'commit', '--allow-empty', '-m', 'c1',
            env=dict(
                os.environ, GIT_COMMITTER_DATE='Wed, Feb 16 14:00 2011 +0100',
            ),
        )
        cmd_output(
            'git', 'commit', '--allow-empty', '-m', 'c2',
            env=dict(
                os.environ, GIT_COMMITTER_DATE='Tue, Feb 15 14:00 2011 +0100',
            ),
        )

    main([cloneable, sandbox.db_path])
    data_count_before = get_metric_data_count(sandbox)
    # Used to raise IntegrityError
    main([cloneable, sandbox.db_path])
    data_count_after = get_metric_data_count(sandbox)
    assert data_count_before == data_count_after


def test_fields_equivalent(tempdir_factory):
    tmpdir = tempdir_factory.get()
    config_filename = os.path.join(tmpdir, 'config.yaml')
    with io.open(config_filename, 'w') as config_file:
        config_file.write(
            'repo: .\n'
            'database: database.db\n'
        )

    config_output = get_options_from_config([
        '--config-filename', config_filename,
    ])
    # pylint:disable=no-member,protected-access
    config_fields = set(config_output._fields)

    argparse_output = get_options_from_argparse(['.', 'database.db'])
    argparse_fields = set(vars(argparse_output))

    # Assert that we got the same fields
    assert (
        argparse_fields - set(('config_filename', 'create_config')) ==
        config_fields
    )

    # Assert that we got the same values
    for field in config_fields:
        assert getattr(config_output, field) == getattr(argparse_output, field)


def test_get_options_from_config_create_config(tempdir_factory):
    tmpdir = tempdir_factory.get()
    with cwd(tmpdir):
        ret = get_options_from_config([
            '--create-config',
            '.',
            'database.db',
        ])

        assert os.path.exists('generate_config.yaml')
        assert yaml.load(io.open('generate_config.yaml').read()) == {
            'repo': '.',
            'database': 'database.db',
        }

        assert ret == GenerateOptions(
            skip_default_metrics=False,
            metric_package_names=[],
            repo='.',
            database='database.db',
        )


def test_get_options_from_config_no_config_file():
    with pytest.raises(SystemExit):
        get_options_from_config(['--config-filename', 'i-dont-exist'])
