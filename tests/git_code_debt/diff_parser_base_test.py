
import testify as T

from git_code_debt.diff_parser_base import FileDiffStat
from git_code_debt.diff_parser_base import Status
from git_code_debt.diff_parser_base import _get_file_diff_stats_from_output

SAMPLE_OUTPUT = """diff --git a/README.md b/README.md
index 17b5d50..6daaaeb 100644
--- a/README.md
+++ b/README.md
@@ -1,4 +1,5 @@
 git-code-debt
 =============

-foo
+bar
+hello world
"""

MERGE_COMMIT_OUTPUT = """commit 42a3a7c8b2141a5d8069e7b83e744d13d335fa17
Merge: c784960 f229b4c
Author: Cameron Paul <cpaul37@gmail.com>
Date:   Thu Nov 14 13:58:49 2013 -0800

    Merge branch 'master' of github.com:asottile/git-code-debt
"""

FILE_ADDED_COMMIT = """commit c1fa89d4f38a9f8784495d38c8c385977178cb3d
Author: Anthony Sottile <asottile@umich.edu>
Date:   Thu Nov 14 11:10:29 2013 -0800

    Added yaml config loading.

diff --git a/example_config.yaml b/example_config.yaml
new file mode 100644
index 0000000..dc7827c
--- /dev/null
+++ b/example_config.yaml
@@ -0,0 +1,4 @@
+
+# Git repo url
+foo
+bar
"""

FILE_REMOVED_COMMIT = """commit f229b4c3e7aded483dab246af49396c538c0ce04
Author: Anthony Sottile <asottile@umich.edu>
Date:   Thu Nov 14 13:35:00 2013 -0800

    Revert adding config

diff --git a/example_config.yaml b/example_config.yaml
deleted file mode 100644
index dc7827c..0000000
--- a/example_config.yaml
+++ /dev/null
@@ -1,4 +0,0 @@
-
-# Git repo url
-foo
-bar
"""

class TestDiffParser(T.TestCase):

    def test_get_file_diff_stats_from_output(self):
        ret = _get_file_diff_stats_from_output(SAMPLE_OUTPUT)
        T.assert_equal(
            ret,
            [FileDiffStat(
                'README.md',
                ['bar', 'hello world'],
                ['foo'],
                Status.ALREADY_EXISTING,
            )]
        )

    def test_does_not_choke_on_empty(self):
        ret = _get_file_diff_stats_from_output(MERGE_COMMIT_OUTPUT)
        T.assert_equal(ret, [])

    def test_added_file(self):
        ret = _get_file_diff_stats_from_output(FILE_ADDED_COMMIT)
        T.assert_equal(
            ret,
            [FileDiffStat(
                'example_config.yaml',
                ['', '# Git repo url', 'foo', 'bar'],
                [],
                Status.ADDED,
            )],
        )

    def test_removed_file(self):
        ret = _get_file_diff_stats_from_output(FILE_REMOVED_COMMIT)
        T.assert_equal(
            ret,
            [FileDiffStat(
                'example_config.yaml',
                [],
                ['', '# Git repo url', 'foo', 'bar'],
                Status.DELETED,
            )],
        )
