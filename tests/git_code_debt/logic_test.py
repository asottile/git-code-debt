
import testify as T

from git_code_debt.create_tables import get_metric_ids
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.logic import get_metric_mapping
from testing.base_classes.sandbox_test_case import SandboxTestCase


class TestLogic(SandboxTestCase):

    def test_get_metric_mapping(self):
        with self.db() as db:
            ret = get_metric_mapping(db)

            T.assert_equal(set(ret.keys()), set(get_metric_ids(get_metric_parsers())))
