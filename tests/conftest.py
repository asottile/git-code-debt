from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import contextlib
import io
import os.path
import pytest
import sqlite3
import subprocess

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import populate_metric_ids
from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import COMMIT_FORMAT
from git_code_debt_util import five
from git_code_debt_util.subprocess import cmd_output
from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.cwd import cwd


@pytest.yield_fixture
def tmpdir_factory(tmpdir):
    class TmpdirFactory(object):
        def __init__(self):
            self.tmpdir_count = 0

        def get(self):
            path = os.path.join(tmpdir.strpath, five.text(self.tmpdir_count))
            self.tmpdir_count += 1
            os.mkdir(path)
            return path

    yield TmpdirFactory()


class Sandbox(collections.namedtuple('Sandbox', ['directory'])):
    __slots__ = ()

    @property
    def db_path(self):
        return os.path.join(self.directory, 'db.db')

    @contextlib.contextmanager
    def db(self):
        with sqlite3.connect(self.db_path) as db:
            yield db


@pytest.yield_fixture
def sandbox(tmpdir_factory):
    ret = Sandbox(tmpdir_factory.get())
    with ret.db() as db:
        create_schema(db)
        populate_metric_ids(db, tuple(), False)

    yield ret


@pytest.yield_fixture
def cloneable(tmpdir_factory):
    repo_path = tmpdir_factory.get()
    with cwd(repo_path):
        subprocess.check_call(['git', 'init', '.'])
        subprocess.check_call(['touch', 'foo.py'])
        subprocess.check_call(['git', 'add', '.'])
        subprocess.check_call(['git', 'commit', '-m', 'foo'])

    yield repo_path


@pytest.yield_fixture
def cloneable_with_commits(cloneable):
    commits = []

    def make_commit(filename, contents):
        with io.open(filename, 'w') as file_obj:
            file_obj.write(contents)

        subprocess.check_call(['git', 'add', filename])
        subprocess.check_call([
            'git', 'commit', '-m', 'Add {0}'.format(filename),
        ])
        output = cmd_output('git', 'show', COMMIT_FORMAT)
        sha, date, author = output.splitlines()[:3]
        commits.append(Commit(sha, int(date), author))

    with cwd(cloneable):
        make_commit('test.py', 'import foo\nimport bar\n')
        make_commit('foo.tmpl', '#import foo\b#import bar\n')

    yield auto_namedtuple(path=cloneable, commits=commits)
