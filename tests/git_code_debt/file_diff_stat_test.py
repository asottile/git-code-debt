
import testify as T

from git_code_debt.discovery import get_metric_parsers
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output

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

COMMIT_ENDING_WITH_BINARY_FILES = """diff --git a/htdocs/css/base.css b/htdocs/css/base.css
index f0f7eac..ca3d0a2 100644
--- a/htdocs/css/base.css
+++ b/htdocs/css/base.css
@@ -18,7 +18,7 @@ DIV, TD, P {
+foo
diff --git a/htdocs/i/p.gif b/htdocs/i/p.gif
new file mode 100644
index 0000000..35d42e8
Binary files /dev/null and b/htdocs/i/p.gif differ
"""

COMMIT_WITH_TERRIBLE = """commit blahblahblah

diff --git a/herpderp b/herpderp
index herp...derp
--- a/herpderp
+++ b/herpderp
+\r+
"""

class TestDiffParser(T.TestCase):

    def test_get_file_diff_stats_from_output(self):
        ret = get_file_diff_stats_from_output(SAMPLE_OUTPUT)
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
        ret = get_file_diff_stats_from_output(MERGE_COMMIT_OUTPUT)
        T.assert_equal(ret, [])

    def test_added_file(self):
        ret = get_file_diff_stats_from_output(FILE_ADDED_COMMIT)
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
        ret = get_file_diff_stats_from_output(FILE_REMOVED_COMMIT)
        T.assert_equal(
            ret,
            [FileDiffStat(
                'example_config.yaml',
                [],
                ['', '# Git repo url', 'foo', 'bar'],
                Status.DELETED,
            )],
        )

    def test_binary_files(self):
        ret = get_file_diff_stats_from_output(COMMIT_ENDING_WITH_BINARY_FILES)
        T.assert_length(ret, 1)

    def test_commit_with_terrible(self):
        ret = get_file_diff_stats_from_output(COMMIT_WITH_TERRIBLE)
        T.assert_length(ret[0].lines_added, 1)

class TestAllMetricParsersDefinePossibleMetrics(T.TestCase):

    def test_all_have_possible_metrics(self):
        for metric_parser_cls in get_metric_parsers():
            try:
                assert metric_parser_cls().get_possible_metric_ids()
            except Exception:
                raise AssertionError(
                    '{0} does not implement get_possible_metric_ids'.format(
                        metric_parser_cls.__name__
                    )
                )
