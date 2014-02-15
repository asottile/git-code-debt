
import testify as T

from git_code_debt.parse_diff_stat import get_stats_from_output
from testing.base_classes.test import test

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

@test
def test_insertions_and_deletions():
    ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS_AND_DELETIONS)
    T.assert_equal(ret, 0)

@test
def test_insertions():
    ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS)
    T.assert_equal(ret, 28)

@test
def test_deletions():
    ret = get_stats_from_output(OUTPUT_WITH_DELETIONS)
    T.assert_equal(ret, -24)

@test
def test_empty_string():
    ret = get_stats_from_output('')
    T.assert_equal(ret, 0)
