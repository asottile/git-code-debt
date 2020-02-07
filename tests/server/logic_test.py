from git_code_debt import write_logic
from git_code_debt.logic import get_metric_mapping
from git_code_debt.metric import Metric
from git_code_debt.repo_parser import Commit
from git_code_debt.server.logic import get_first_data_timestamp


def test_no_data_returns_zero(sandbox):
    with sandbox.db() as db:
        assert get_first_data_timestamp('PythonImportCount', db=db) == 0


def insert(db, sha, timestamp, value, has_data=True):
    metric_mapping = get_metric_mapping(db)
    write_logic.insert_metric_values(
        db,
        {metric_mapping['PythonImportCount']: value},
        {metric_mapping['PythonImportCount']: has_data},
        Commit(sha, timestamp),
    )


def insert_metric_changes(db, sha, change):
    metric_mapping = get_metric_mapping(db)
    write_logic.insert_metric_changes(
        db,
        (Metric('PythonImportCount', change),),
        metric_mapping,
        Commit(sha, 0),
    )


def test_some_data_returns_first_timestamp(sandbox):
    with sandbox.db() as db:
        insert(db, '1' * 40, 1111, 0, has_data=False)
        assert get_first_data_timestamp('PythonImportCount', db=db) == 0


def test_some_data_returns_last_zero_before_data(sandbox):
    with sandbox.db() as db:
        insert(db, '1' * 40, 1111, 0, has_data=False)
        insert(db, '2' * 40, 2222, 0, has_data=False)
        insert(db, '3' * 40, 3333, 1)
        insert_metric_changes(db, '3' * 40, 1)
        assert get_first_data_timestamp('PythonImportCount', db=db) == 3333


def test_first_commit_introduces_data(sandbox):
    with sandbox.db() as db:
        insert(db, '1' * 40, 1111, 1)
        insert_metric_changes(db, '1' * 40, 1)
        insert(db, '2' * 40, 2222, 2)
        insert_metric_changes(db, '2' * 40, 1)
        assert get_first_data_timestamp('PythonImportCount', db=db) == 1111
