
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status


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

FILE_REMOVED_COMMIT = """diff --git a/example_config.yaml b/example_config.yaml
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

SAMPLE_OUTPUT_MULTIPLE_FILES = FILE_ADDED_COMMIT + FILE_REMOVED_COMMIT

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
index herp...derp 100644
--- a/herpderp
+++ b/herpderp
+\r+
"""

COMMIT_ADDING_SYMLINK = """diff --git a/pa2 b/pa2
new file mode 120000
index 0000000..989c69d
--- /dev/null
+++ b/pa2
@@ -0,0 +1 @@
+apache/html1/2mJe7Zhz/pa2/
\ No newline at end of file
"""

COMMIT_REMOVING_SYMLINK = """diff --git a/pa2 b/pa2
deleted file mode 120000
index 989c69d..0000000
--- a/pa2
+++ /dev/null
@@ -1 +0,0 @@
-apache/html1/2mJe7Zhz/pa2/
\ No newline at end of file
"""

COMMIT_MOVING_SYMLINK = """diff --git a/pa2 b/pa2
index 989c69d..7b8b995 120000
--- a/pa2
+++ b/pa2
@@ -1 +1 @@
-apache/html1/2mJe7Zhz/pa2/
\ No newline at end of file
+apache/
\ No newline at end of file
"""

MULTIPLE_EMPTY_FILES = """diff --git a/foo/__init__.py b/foo/__init__.py
new file mode 100644
index 0000000..e69de29
diff --git a/bar/__init__.py b/bar/__init__.py
new file mode 100644
index 0000000..e69de29
"""

MODE_CHANGE_COMMIT = """diff --git a/EECS485PA3_W13.pdf b/EECS485PA3_W13.pdf
old mode 100755
new mode 100644
"""

ADD_SUBMODULE_COMMIT = """diff --git a/.gitmodules b/.gitmodules
index e69de29..c8af28a 100644
--- a/.gitmodules
+++ b/.gitmodules
@@ -0,0 +1,3 @@
+[submodule "verifycppbraces"]
+       path = verifycppbraces
+       url = git://github.com/asottile/verifycppbraces.git
diff --git a/verifycppbraces b/verifycppbraces
new file mode 160000
index 0000000..72053d8
--- /dev/null
+++ b/verifycppbraces
@@ -0,0 +1 @@
+Subproject commit 72053d85133aa854e2762a4b604976da825750fb
"""

REMOVE_SUBMODULE_COMMIT = """diff --git a/.gitmodules b/.gitmodules
index e69de29..c8af28a 100644
--- a/.gitmodules
+++ b/.gitmodules
@@ -0,0 +1,3 @@
-[submodule "verifycppbraces"]
-       path = verifycppbraces
-       url = git://github.com/asottile/verifycppbraces.git
diff --git a/verifycppbraces b/verifycppbraces
deleted file mode 160000
index 72053d8..0000000
--- a/verifycppbraces
+++ /dev/null
@@ -0,0 +1 @@
-Subproject commit 72053d85133aa854e2762a4b604976da825750fb
"""

BUMP_SUBMODULE_COMMIT = """diff --git a/verifycppbraces b/verifycppbraces
index 72053d8..d7c12e2 160000
--- a/verifycppbraces
+++ b/verifycppbraces
@@ -1 +1 @@
-Subproject commit 72053d85133aa854e2762a4b604976da825750fb
+Subproject commit d7c12e294428b60667dedd46ed7f00c04e36b7e4
"""

ADD_BINARY_COMMIT = """diff --git a/foo.pdf b/foo.pdf
new file mode 100644
index 0000000..2aaa277
Binary files /dev/null and b/foo.pdf differ
"""

REMOVE_BINARY_COMMIT = """diff --git a/foo.pdf b/foo.pdf
deleted file mode 100644
index 2aaa277..0000000
Binary files a/foo.pdf and /dev/null differ
"""

MODIFY_BINARY_COMMIT = """diff --git a/foo.pdf b/foo.pdf
index 2aaa277..86e041d 100644
Binary files a/foo.pdf and b/foo.pdf differ
"""


def test_get_file_diff_stats_from_output():
    ret = get_file_diff_stats_from_output(SAMPLE_OUTPUT)
    assert ret == [
        FileDiffStat(
            'README.md',
            ['bar', 'hello world'],
            ['foo'],
            Status.ALREADY_EXISTING,
        ),
    ]


def test_does_not_choke_on_empty():
    ret = get_file_diff_stats_from_output(MERGE_COMMIT_OUTPUT)
    assert ret == []


def test_added_file():
    ret = get_file_diff_stats_from_output(FILE_ADDED_COMMIT)
    assert ret == [
        FileDiffStat(
            'example_config.yaml',
            ['', '# Git repo url', 'foo', 'bar'],
            [],
            Status.ADDED,
        ),
    ]


def test_removed_file():
    ret = get_file_diff_stats_from_output(FILE_REMOVED_COMMIT)
    assert ret == [
        FileDiffStat(
            'example_config.yaml',
            [],
            ['', '# Git repo url', 'foo', 'bar'],
            Status.DELETED,
        ),
    ]


def test_removed_and_added():
    ret = get_file_diff_stats_from_output(SAMPLE_OUTPUT_MULTIPLE_FILES)
    assert ret == [
        FileDiffStat(
            'example_config.yaml',
            ['', '# Git repo url', 'foo', 'bar'],
            [],
            Status.ADDED,
        ),
        FileDiffStat(
            'example_config.yaml',
            [],
            ['', '# Git repo url', 'foo', 'bar'],
            Status.DELETED,
        ),
    ]


def test_binary_files():
    ret = get_file_diff_stats_from_output(COMMIT_ENDING_WITH_BINARY_FILES)
    assert ret == [
        FileDiffStat(
            'htdocs/css/base.css',
            ['foo'], [],
            Status.ALREADY_EXISTING,
        ),
        FileDiffStat(
            'htdocs/i/p.gif',
            [], [],
            Status.ADDED,
            special_file=SpecialFile(
                file_type=SpecialFileType.BINARY,
                added='htdocs/i/p.gif',
                removed=None,
            ),
        ),
    ]


def test_commit_with_terrible():
    ret = get_file_diff_stats_from_output(COMMIT_WITH_TERRIBLE)
    assert len(ret[0].lines_added) == 1


def test_all_metric_parsers_have_possible_metrics():
    for metric_parser_cls in get_metric_parsers():
        assert metric_parser_cls().get_possible_metric_ids()


def test_adding_symlink():
    ret = get_file_diff_stats_from_output(COMMIT_ADDING_SYMLINK)
    assert ret == [
        FileDiffStat(
            'pa2',
            [], [],
            Status.ADDED,
            special_file=SpecialFile(
                file_type=SpecialFileType.SYMLINK,
                added='apache/html1/2mJe7Zhz/pa2/',
                removed=None,
            ),
        ),
    ]


def test_removing_symlink():
    ret = get_file_diff_stats_from_output(COMMIT_REMOVING_SYMLINK)
    assert ret == [
        FileDiffStat(
            'pa2',
            [], [],
            Status.DELETED,
            special_file=SpecialFile(
                file_type=SpecialFileType.SYMLINK,
                added=None,
                removed='apache/html1/2mJe7Zhz/pa2/',
            ),
        ),
    ]


def test_moving_symlink():
    ret = get_file_diff_stats_from_output(COMMIT_MOVING_SYMLINK)
    assert ret == [
        FileDiffStat(
            'pa2',
            [], [],
            Status.ALREADY_EXISTING,
            special_file=SpecialFile(
                file_type=SpecialFileType.SYMLINK,
                added='apache/',
                removed='apache/html1/2mJe7Zhz/pa2/',
            ),
        ),
    ]


def test_multiple_empty_files():
    ret = get_file_diff_stats_from_output(MULTIPLE_EMPTY_FILES)
    assert ret == [
        FileDiffStat('foo/__init__.py', [], [], Status.ADDED),
        FileDiffStat('bar/__init__.py', [], [], Status.ADDED),
    ]


def test_mode_change_diff():
    ret = get_file_diff_stats_from_output(MODE_CHANGE_COMMIT)
    assert ret == [
        FileDiffStat('EECS485PA3_W13.pdf', [], [], Status.ALREADY_EXISTING),
    ]


def test_add_submodule():
    ret = get_file_diff_stats_from_output(ADD_SUBMODULE_COMMIT)
    assert ret == [
        FileDiffStat(
            '.gitmodules',
            [
                '[submodule "verifycppbraces"]',
                '       path = verifycppbraces',
                '       url = git://github.com/asottile/verifycppbraces.git',
            ],
            [],
            Status.ALREADY_EXISTING,
        ),
        FileDiffStat(
            'verifycppbraces', [], [], Status.ADDED,
            special_file=SpecialFile(
                file_type=SpecialFileType.SUBMODULE,
                added='72053d85133aa854e2762a4b604976da825750fb',
                removed=None,
            ),
        ),
    ]


def test_remove_submodule():
    ret = get_file_diff_stats_from_output(REMOVE_SUBMODULE_COMMIT)
    assert ret == [
        FileDiffStat(
            '.gitmodules',
            [],
            [
                '[submodule "verifycppbraces"]',
                '       path = verifycppbraces',
                '       url = git://github.com/asottile/verifycppbraces.git',
            ],
            Status.ALREADY_EXISTING,
        ),
        FileDiffStat(
            'verifycppbraces', [], [], Status.DELETED,
            special_file=SpecialFile(
                file_type=SpecialFileType.SUBMODULE,
                added=None,
                removed='72053d85133aa854e2762a4b604976da825750fb',
            ),
        ),
    ]


def test_bump_submodule():
    ret = get_file_diff_stats_from_output(BUMP_SUBMODULE_COMMIT)
    assert ret == [
        FileDiffStat(
            'verifycppbraces', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(
                file_type=SpecialFileType.SUBMODULE,
                added='d7c12e294428b60667dedd46ed7f00c04e36b7e4',
                removed='72053d85133aa854e2762a4b604976da825750fb',
            ),
        ),
    ]


def test_add_binary_commit():
    ret = get_file_diff_stats_from_output(ADD_BINARY_COMMIT)
    assert ret == [
        FileDiffStat(
            'foo.pdf', [], [], Status.ADDED,
            special_file=SpecialFile(
                file_type=SpecialFileType.BINARY,
                added='foo.pdf',
                removed=None,
            ),
        ),
    ]


def test_remove_binary_commit():
    ret = get_file_diff_stats_from_output(REMOVE_BINARY_COMMIT)
    assert ret == [
        FileDiffStat(
            'foo.pdf', [], [], Status.DELETED,
            special_file=SpecialFile(
                file_type=SpecialFileType.BINARY,
                added=None,
                removed='foo.pdf',
            ),
        ),
    ]


def test_modified_binary_commit():
    ret = get_file_diff_stats_from_output(MODIFY_BINARY_COMMIT)
    assert ret == [
        FileDiffStat(
            'foo.pdf',  [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(
                file_type=SpecialFileType.BINARY,
                added='foo.pdf',
                removed='foo.pdf',
            ),
        ),
    ]
