
from git_code_debt.parse_diff_stat import get_stats_from_output

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

def test_insertions_and_deletions():
    ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS_AND_DELETIONS)
    assert ret == 0

def test_insertions():
    ret = get_stats_from_output(OUTPUT_WITH_INSERTIONS)
    assert ret == 28

def test_deletions():
    ret = get_stats_from_output(OUTPUT_WITH_DELETIONS)
    assert ret == -24

def test_empty_string():
    ret = get_stats_from_output('')
    assert ret == 0
