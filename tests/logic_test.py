
import pytest

from git_code_debt.create_tables import get_metric_ids
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.logic import insert_metric_values
from git_code_debt.repo_parser import Commit


sha = 'a' * 40
repo = 'git@github.com:asottile/git-code-debt'


@pytest.mark.integration
def test_get_metric_mapping(sandbox):
    with sandbox.db() as db:
        ret = get_metric_mapping(db)

        assert (
            set(ret.keys()) ==
            set(get_metric_ids(get_metric_parsers()))
        )


@pytest.mark.integration
def test_get_previous_sha_no_previous_sha(sandbox):
    with sandbox.db() as db:
        ret = get_previous_sha(db, repo)
        assert ret is None


def get_fake_metrics(metric_mapping):
    return dict(
        (metric_name, 1) for metric_name in metric_mapping.keys()
    )


def get_fake_commit():
    return Commit(sha, 1, 'foo')


def insert_fake_metrics(db):
    metric_mapping = get_metric_mapping(db)
    metric_values = get_fake_metrics(metric_mapping)
    commit = get_fake_commit()
    insert_metric_values(db, metric_values, metric_mapping, repo, commit)


@pytest.mark.integration
def test_get_previous_sha_previous_existing_sha(sandbox):
    with sandbox.db() as db:
        insert_fake_metrics(db)
        ret = get_previous_sha(db, repo)
        assert ret == sha


@pytest.mark.integration
def test_insert_and_get_metric_values(sandbox):
    with sandbox.db() as db:
        fake_metrics = get_fake_metrics(get_metric_mapping(db))
        fake_commit = get_fake_commit()
        insert_fake_metrics(db)
        assert fake_metrics == get_metric_values(db, fake_commit)
