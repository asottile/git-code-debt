from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.create_tables import get_metric_ids
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.repo_parser import Commit
from git_code_debt.write_logic import insert_metric_values


def test_get_metric_mapping(sandbox):
    with sandbox.db() as db:
        ret = get_metric_mapping(db)

        assert (
            set(ret.keys()) ==
            set(get_metric_ids(get_metric_parsers()))
        )


def test_get_previous_sha_no_previous_sha(sandbox):
    with sandbox.db() as db:
        ret = get_previous_sha(db)
        assert ret is None


def get_fake_metrics(metric_mapping):
    return {metric_name: 1 for metric_name in metric_mapping}


def insert_fake_metrics(db):
    metric_mapping = get_metric_mapping(db)
    metric_values = get_fake_metrics(metric_mapping)
    for sha_part in ('a', 'b', 'c'):
        commit = Commit(sha_part * 40, 1)
        insert_metric_values(db, metric_values, metric_mapping, commit)


def test_get_previous_sha_previous_existing_sha(sandbox):
    with sandbox.db() as db:
        insert_fake_metrics(db)
        ret = get_previous_sha(db)
        assert ret == 'c' * 40


def test_insert_and_get_metric_values(sandbox):
    with sandbox.db() as db:
        fake_metrics = get_fake_metrics(get_metric_mapping(db))
        insert_fake_metrics(db)
        assert fake_metrics == get_metric_values(db, 'a' * 40)
