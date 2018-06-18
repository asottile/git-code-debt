from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import io
import os.path
import re
import sqlite3

import pytest

from git_code_debt.generate import _get_metrics_inner
from git_code_debt.generate import create_schema
from git_code_debt.generate import get_options_from_config
from git_code_debt.generate import increment_metric_values
from git_code_debt.generate import main
from git_code_debt.generate import mapper
from git_code_debt.generate import populate_metric_ids
from git_code_debt.metric import Metric
from git_code_debt.metrics.lines import LinesOfCodeParser
from git_code_debt.repo_parser import RepoParser
from git_code_debt.util.subprocess import cmd_output
from testing.utilities.cwd import cwd


def test_increment_metrics_first_time():
    metric_values = collections.Counter()
    metrics = [Metric('foo', 1), Metric('bar', 2)]
    increment_metric_values(metric_values, {'foo': 0, 'bar': 1}, metrics)
    assert metric_values == {0: 1, 1: 2}


def test_increment_metrics_already_there():
    metric_values = collections.Counter({0: 2, 1: 3})
    metrics = [Metric('foo', 1), Metric('bar', 2)]
    increment_metric_values(metric_values, {'foo': 0, 'bar': 1}, metrics)
    assert metric_values == {0: 3, 1: 5}


def test_get_metrics_inner_first_commit(cloneable_with_commits):
    repo_parser = RepoParser(cloneable_with_commits.path)
    with repo_parser.repo_checked_out():
        metrics = _get_metrics_inner((
            None, cloneable_with_commits.commits[0],
            repo_parser, [LinesOfCodeParser], re.compile(b'^$'),
        ))
        assert Metric(name='TotalLinesOfCode', value=0) in metrics


def test_get_metrics_inner_nth_commit(cloneable_with_commits):
    repo_parser = RepoParser(cloneable_with_commits.path)
    with repo_parser.repo_checked_out():
        metrics = _get_metrics_inner((
            cloneable_with_commits.commits[-2],
            cloneable_with_commits.commits[-1],
            repo_parser, [LinesOfCodeParser], re.compile(b'^$'),
        ))
        assert Metric(name='TotalLinesOfCode', value=2) in metrics


def square(x):
    return x * x


@pytest.mark.parametrize('jobs', (1, 4))
def test_mapper(jobs):
    ret = tuple(mapper(jobs)(square, (3, 5, 9)))
    assert ret == (9, 25, 81)


def test_generate_integration(sandbox, cloneable):
    main(('-C', sandbox.gen_config(repo=cloneable)))


def test_main_database_does_not_exist(sandbox, cloneable):
    new_db_path = os.path.join(sandbox.directory, 'new.db')
    cfg = sandbox.gen_config(database=new_db_path, repo=cloneable)
    assert not main(('-C', cfg))
    assert os.path.exists(new_db_path)


def get_metric_data_count(sandbox):
    with sandbox.db() as db:
        return db.execute('SELECT COUNT(*) FROM metric_data').fetchone()[0]


def test_generate_integration_previous_data(sandbox, cloneable_with_commits):
    cfg = sandbox.gen_config(repo=cloneable_with_commits.path)
    main(('-C', cfg))
    before_data_count = get_metric_data_count(sandbox)
    assert before_data_count > 0
    main(('-C', cfg))
    after_data_count = get_metric_data_count(sandbox)
    assert before_data_count == after_data_count


def test_generate_new_data_created(sandbox, cloneable_with_commits):
    cfg = sandbox.gen_config(repo=cloneable_with_commits.path)
    main(('-C', cfg))
    before_data_count = get_metric_data_count(sandbox)
    # Add some commits
    with cwd(cloneable_with_commits.path):
        with open('new_file.py', 'w') as f:
            f.write('# test\n')
        cmd_output('git', 'add', 'new_file.py')
        cmd_output('git', 'commit', '-m', 'bar')
    main(('-C', cfg))
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

    cfg = sandbox.gen_config(repo=cloneable)
    main(('-C', cfg))
    data_count_before = get_metric_data_count(sandbox)
    # Used to raise IntegrityError
    main(('-C', cfg))
    data_count_after = get_metric_data_count(sandbox)
    assert data_count_before == data_count_after


def test_moves_handled_properly(sandbox, cloneable):
    with cwd(cloneable):
        with io.open('f', 'w') as f:
            f.write('foo\nbar\nbaz\n')
        cmd_output('git', 'add', 'f')
        cmd_output('git', 'commit', '-m', 'add f')
        cmd_output('git', 'mv', 'f', 'g')
        cmd_output('git', 'commit', '-m', 'move f to g')

    # Used to raise AssertionError
    assert not main(('-C', sandbox.gen_config(repo=cloneable)))


def test_internal_zero_populated(sandbox, cloneable):
    with cwd(cloneable):
        with io.open('f.py', 'w') as f:
            f.write('# hello world\n')
        cmd_output('git', 'add', 'f.py')
        cmd_output('git', 'commit', '-m', 'add f')
        cmd_output('git', 'rm', 'f.py')
        cmd_output('git', 'commit', '-m', 'remove f')
        cmd_output('git', 'revert', 'HEAD', '--no-edit')

    assert not main(('-C', sandbox.gen_config(repo=cloneable)))
    with sandbox.db() as db:
        query = (
            'SELECT running_value\n'
            'FROM metric_data\n'
            'INNER JOIN metric_names ON\n'
            '    metric_data.metric_id == metric_names.id\n'
            'WHERE name = "TotalLinesOfCode_python"\n'
        )
        vals = [x for x, in db.execute(query).fetchall()]
        assert vals == [1, 0, 1]


def test_exclude_pattern(sandbox, cloneable_with_commits):
    cfg = sandbox.gen_config(
        repo=cloneable_with_commits.path, exclude=r'\.tmpl$',
    )
    assert not main(('-C', cfg))
    with sandbox.db() as db:
        query = (
            'SELECT running_value\n'
            'FROM metric_data\n'
            'INNER JOIN metric_names ON\n'
            '    metric_data.metric_id == metric_names.id\n'
            'WHERE sha = ? AND name = "TotalLinesOfCode"\n'
        )
        sha = cloneable_with_commits.commits[-1].sha
        val, = db.execute(query, (sha,)).fetchone()
        # 2 lines of code from test.py, 0 lines from foo.tmpl (2 lines)
        assert val == 2


def test_get_options_from_config_no_config_file():
    with pytest.raises(SystemExit):
        get_options_from_config('i-dont-exist')


def test_create_schema(tmpdir):
    with sqlite3.connect(tmpdir.join('db.db').strpath) as db:
        create_schema(db)

        results = db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'",
        ).fetchall()
        table_names = [table_name for table_name, in results]

        assert 'metric_names' in table_names
        assert 'metric_data' in table_names


def test_populate_metric_ids(tmpdir):
    with sqlite3.connect(tmpdir.join('db.db').strpath) as db:
        create_schema(db)
        populate_metric_ids(db, (), False)

        results = db.execute('SELECT * FROM metric_names').fetchall()
        # Smoke test assertion
        assert results
