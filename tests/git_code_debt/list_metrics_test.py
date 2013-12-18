
import __builtin__

import mock
import testify as T

from git_code_debt.list_metrics import main


@T.suite('integration')
class TestListMetricsSmoke(T.TestCase):

    def test_smoke(self):
        # This test is just to make sure that it doesn't fail catastrophically
        with mock.patch.object(__builtin__, 'print', autospec=True) as print_mock:
            main([])
            T.assert_true(print_mock.called)
