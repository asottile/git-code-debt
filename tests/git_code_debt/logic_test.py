
import testify as T

from git_code_debt.create_tables import get_metric_ids
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.logic import insert_metric_values
from git_code_debt.repo_parser import Commit
from testing.base_classes.sandbox_test_case import SandboxTestCase


class TestLogic(SandboxTestCase):

    sha = 'a' * 40
    repo = 'git@github.com:asottile/git-code-debt'

    def test_get_metric_mapping(self):
        with self.db() as db:
            ret = get_metric_mapping(db)

            T.assert_equal(set(ret.keys()), set(get_metric_ids(get_metric_parsers())))

    def test_get_previous_sha_no_previous_sha(self):
        with self.db() as db:
            ret = get_previous_sha(db, self.repo)
            T.assert_is(ret, None)

    def get_fake_metrics(self, metric_mapping):
        return dict(
            (metric_name, 1) for metric_name in metric_mapping.keys()
        )

    def get_fake_commit(self):
        return Commit(self.sha, 1, 'foo')

    def insert_fake_metrics(self, db):
        metric_mapping = get_metric_mapping(db)
        metric_values = self.get_fake_metrics(metric_mapping)
        commit = self.get_fake_commit()
        insert_metric_values(db, metric_values, metric_mapping, self.repo, commit)

    def test_get_previous_sha_previous_existing_sha(self):
        with self.db() as db:
            self.insert_fake_metrics(db)
            ret = get_previous_sha(db, self.repo)
            T.assert_equal(ret, self.sha)

    def test_insert_and_get_metric_values(self):
        with self.db() as db:
            fake_metrics = self.get_fake_metrics(get_metric_mapping(db))
            fake_commit = self.get_fake_commit()
            self.insert_fake_metrics(db)
            T.assert_equal(fake_metrics, get_metric_values(db, fake_commit))
