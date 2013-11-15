
import testify as T

from git_code_debt.generate import get_stats_from_output

OUTPUT_WITH_INSERTIONS_AND_DELETIONS = '''
14b4fc0 Made names for js and css consistent
 git_code_debt_server/static/css/banker.css        |    4 ----
 git_code_debt_server/static/css/git_code_debt.css |    4 ++++
 git_code_debt_server/static/js/banker.js          |   24 ---------------------
 git_code_debt_server/static/js/git_code_debt.js   |   24 +++++++++++++++++++++
 4 files changed, 28 insertions(+), 28 deletions(-)
'''

OUTPUT_WITH_DELETIONS = '''
14b4fc0 Made names for js and css consistent
 git_code_debt_server/static/js/git_code_debt.js   |   24 +++++++++++++++++++++
 4 files changed, 24 deletions(-)
'''

OUTPUT_WITH_INSERTIONS = '''
14b4fc0 Made names for js and css consistent
 git_code_debt_server/static/css/git_code_debt.css |    4 ++++
 git_code_debt_server/static/js/git_code_debt.js   |   24 +++++++++++++++++++++
 4 files changed, 28 insertions(+)
'''

class TestGetStatsFromOutput(T.TestCase):

    def test_insertions_and_deletions(self):
        ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS_AND_DELETIONS)
        T.assert_equal(ret, 0)

    def test_insertions(self):
        ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS)
        T.assert_equal(ret, 28)

    def test_deletions(self):
        ret = get_stats_from_output(OUTPUT_WITH_DELETIONS)
        T.assert_equal(ret, -24)
