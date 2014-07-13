from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import insert_metric_values
from git_code_debt.repo_parser import Commit
from git_code_debt.server.logic.metrics import get_first_data_timestamp


def test_no_data_returns_zero(sandbox):
    with sandbox.db() as db:
        assert get_first_data_timestamp('PythonImportCount', db=db) == 0


def insert(db, sha, timestamp, value):
    metric_mapping = get_metric_mapping(db)
    insert_metric_values(
        db,
        {'PythonImportCount': value},
        metric_mapping,
        Commit(sha, timestamp, None),
    )


def test_some_data_returns_first_timestamp(sandbox):
    with sandbox.db() as db:
        insert(db, '1' * 40, 1111, 0)
        assert get_first_data_timestamp('PythonImportCount', db=db) == 1111


def test_some_data_returns_last_zero_before_data(sandbox):
    with sandbox.db() as db:
        insert(db, '1' * 40, 1111, 0)
        insert(db, '2' * 40, 2222, 0)
        insert(db, '3' * 40, 3333, 1)
        assert get_first_data_timestamp('PythonImportCount', db=db) == 2222
