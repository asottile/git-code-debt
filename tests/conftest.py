
from __future__ import absolute_import

import contextlib
import os.path
import pytest
import sqlite3

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import populate_metric_ids
from git_code_debt.repo_parser import RepoParser


class Sandbox(object):
    def __init__(self, directory):
        self.directory = directory

    @property
    def db_path(self):
        return os.path.join(self.directory, 'db.db')

    @contextlib.contextmanager
    def db(self):
        with sqlite3.connect(self.db_path) as db:
            yield db


@pytest.fixture
def sandbox(tmpdir):
    ret = Sandbox(tmpdir.strpath)
    with ret.db() as db:
        create_schema(db)
        populate_metric_ids(db, tuple(), False)

    return ret


@pytest.yield_fixture(scope='session')
def cloneable():
    repo_parser = RepoParser('git://github.com/asottile/git-code-debt')
    with repo_parser.repo_checked_out():
        yield repo_parser.tempdir
