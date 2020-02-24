import contextlib
import os.path
import sqlite3
import subprocess
from typing import NamedTuple

import pytest

from git_code_debt.generate import create_schema
from git_code_debt.generate import populate_metric_ids
from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import COMMIT_FORMAT
from git_code_debt.util import yaml
from git_code_debt.util.subprocess import cmd_output
from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.cwd import cwd


@pytest.fixture
def tempdir_factory(tmpdir):
    class TmpdirFactory:
        def __init__(self):
            self.tmpdir_count = 0

        def get(self):
            path = tmpdir.join(str(self.tmpdir_count)).strpath
            self.tmpdir_count += 1
            os.mkdir(path)
            return path

    yield TmpdirFactory()


class Sandbox(NamedTuple):
    directory: str


@property
def db_path(self):
    return os.path.join(self.directory, 'db.db')


Sandbox.db_path = db_path


def gen_config(self, **data):
    path = os.path.join(self.directory, 'generate_config.yaml')
    with open(path, 'w') as f:
        yaml.dump(
            dict({'database': self.db_path}, **data),
            f,
            encoding=None,
            default_flow_style=False,
        )
    return path


Sandbox.gen_config = gen_config


@contextlib.contextmanager
def db(self):
    with sqlite3.connect(self.db_path) as db:
        yield db


Sandbox.db = db


@pytest.fixture
def sandbox(tempdir_factory):
    ret = Sandbox(tempdir_factory.get())
    with ret.db() as db:
        create_schema(db)
        populate_metric_ids(db, [], False)

    yield ret


@pytest.fixture
def cloneable(tempdir_factory):
    repo_path = tempdir_factory.get()
    with cwd(repo_path):
        subprocess.check_call(('git', 'init', '.'))
        subprocess.check_call(('git', 'commit', '-m', 'foo', '--allow-empty'))

    yield repo_path


@pytest.fixture
def cloneable_with_commits(cloneable):
    commits = []

    def append_commit():
        output = cmd_output('git', 'show', COMMIT_FORMAT)
        sha, date = output.splitlines()[:2]
        commits.append(Commit(sha, int(date)))

    def make_commit(filename, contents):
        # Make the graph tests more deterministic
        # import time; time.sleep(2)
        with open(filename, 'w') as file_obj:
            file_obj.write(contents)

        subprocess.check_call(('git', 'add', filename))
        subprocess.check_call((
            'git', 'commit', '-m', f'Add {filename}',
        ))
        append_commit()

    with cwd(cloneable):
        # Append a commit for the inital commit
        append_commit()
        make_commit('bar.py', '')
        make_commit('baz.py', '')
        make_commit('test.py', 'import foo\nimport bar\n')
        make_commit('foo.tmpl', '#import foo\n#import bar\n')

    yield auto_namedtuple(path=cloneable, commits=commits)
