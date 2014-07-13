from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import os
import pytest
import sqlite3

from git_code_debt.generate import increment_metric_values
from git_code_debt.generate import main
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
    with pytest.raises(sqlite3.IntegrityError):
        main([cloneable, sandbox.db_path])
    data_count_after = get_metric_data_count(sandbox)
    assert data_count_before == data_count_after
