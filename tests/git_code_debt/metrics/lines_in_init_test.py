
import testify as T

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.lines_in_init import Python__init__LineCount

class TestPython__init__LineCount(T.TestCase):

   def test_lines_in_init(self):
       parser = Python__init__LineCount()
       input = [
           FileDiffStat(
               'testing/__init__.py',
               ['from .foo import bar'],
               [],
               None,
           ),
       ]
       metrics = list(parser.get_metrics_from_stat(input))
       T.assert_equal(metrics, [Metric('Python__init__LineCount', 1)])
