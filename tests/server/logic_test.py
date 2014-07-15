from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.logic import get_metric_mapping
from git_code_debt.repo_parser import Commit
from git_code_debt.server.logic import get_all_data
from git_code_debt.server.logic import get_first_data_timestamp
from git_code_debt.server.logic import get_previous_sha
from git_code_debt.write_logic import insert_metric_values


def test_no_data_returns_zero(sandbox):
    with sandbox.db() as db:
        assert get_first_data_timestamp('PythonImportCount', db=db) == 0


def insert(db, sha, timestamp, value):
    metric_mapping = get_metric_mapping(db)
    insert_metric_values(
        db,
        {'PythonImportCount': value, 'TODOCount': value},
        metric_mapping,
        Commit(sha, timestamp),
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


def _insert_all_data_test_data(db):
    insert(db, '1' * 40, 1111, 1)
    insert(db, '2' * 40, 2222, 2)
    insert(db, '3' * 40, 3333, 3)


def test_get_all_data_inclusive(sandbox):
    with sandbox.db() as db:
        _insert_all_data_test_data(db)
        ret = get_all_data('PythonImportCount', 0, 4444, db=db)

    assert ret == (
        ('1' * 40, 1, 1111),
        ('2' * 40, 2, 2222),
        ('3' * 40, 3, 3333),
    )


def test_get_all_data_edge_left(sandbox):
    with sandbox.db() as db:
        _insert_all_data_test_data(db)
        ret = get_all_data('PythonImportCount', 1111, 4444, db=db)

    assert ret == (
        ('1' * 40, 1, 1111),
        ('2' * 40, 2, 2222),
        ('3' * 40, 3, 3333),
    )


def test_get_all_data_edge_right(sandbox):
    with sandbox.db() as db:
        _insert_all_data_test_data(db)
        ret = get_all_data('PythonImportCount', 0, 3333, db=db)

    assert ret == (
        ('1' * 40, 1, 1111),
        ('2' * 40, 2, 2222),
    )


def test_get_all_data_empty_set(sandbox):
    with sandbox.db() as db:
        ret = get_all_data('PythonImportCount', 0, 1, db=db)

    assert ret == ()


def test_get_previous_sha_first_sha(sandbox):
    with sandbox.db() as db:
        _insert_all_data_test_data(db)
        ret = get_previous_sha('1' * 40, db=db)

    assert ret is None


def test_get_previous_sha_not_first(sandbox):
    with sandbox.db() as db:
        _insert_all_data_test_data(db)
        ret = get_previous_sha('2' * 40, db=db)

    assert ret == '1' * 40
