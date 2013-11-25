
import collections
import testify as T

from git_code_debt.generate import increment_metric_values
from git_code_debt.generate import main
from git_code_debt.metric import Metric
from testing.base_classes.sandbox_test_case import SandboxTestCase

class TestIncrementMetricValues(T.TestCase):

    def test_increment_metrics_first_time(self):
        metrics = collections.defaultdict(int)
        increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
        T.assert_equal(metrics, {'foo': 1, 'bar': 2})

    def test_increment_metrics_already_there(self):
        metrics = collections.defaultdict(int, {'foo': 2, 'bar': 3})
        increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
        T.assert_equal(metrics, {'foo': 3, 'bar': 5})

@T.suite('integration')
class TestGenerateIntegration(SandboxTestCase):

    def test_generate_integration(self):
        main(['.', self.db_path])
