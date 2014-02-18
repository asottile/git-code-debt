
import collections
import os.path
import re


class Status(object):
    ADDED = object()
    DELETED = object()
    ALREADY_EXISTING = object()


Submodule = collections.namedtuple('Submodule', ['added', 'removed'])
Symlink = collections.namedtuple('Symlink', ['added', 'removed'])


class FileDiffStat(collections.namedtuple(
    'FileStat',
    ['path', 'lines_added', 'lines_removed', 'status', 'symlink'],
)):
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        # Default symlink to None in the case it is not provided (mostly for
        # backwards compatibility)
        kwargs.setdefault('symlink', None)
        return super(FileDiffStat, cls).__new__(cls, *args, **kwargs)

    @property
    def extension(self):
        return os.path.splitext(self.path)[1]

    @property
    def filename(self):
        return os.path.split(self.path)[1]


SYMLINK_MODE = '120000'


def _to_file_diff_stat(file_diff):
    NEWLINE = '\n'
    lines = file_diff.split(NEWLINE)
    diff_line_filename = lines[0].split()[-1].lstrip('b').lstrip('/')
    in_diff = False
    mode = None
    status = None
    lines_added = []
    lines_removed = []

    for line in lines[1:]:
        # Mode will be indicated somewhere between diff --git line
        # and the file added / removed lines
        # It has these forms:
        # 1. 'new file mode 100644'
        # 2. 'deleted file mode 100644'
        # 3. 'index dc7827c..7b8b995 100644'
        # 4. 'old mode 100755'
        #    'new mode 100644'
        if line.startswith('new file mode '):
            assert status is None
            assert mode is None
            status = Status.ADDED
            mode = line.split()[-1]
        elif line.startswith('deleted file mode '):
            assert status is None
            assert mode is None
            status = Status.DELETED
            mode = line.split()[-1]
        elif line.startswith('new mode '):
            assert status is None
            assert mode is None
            status = Status.ALREADY_EXISTING
            mode = line.split()[-1]
        elif line.startswith('index') and len(line.split()) == 3:
            assert status is None
            assert mode is None
            status = Status.ALREADY_EXISTING
            mode = line.split()[-1]
        # A diff contains lines that look like:
        # --- foo/bar
        # +++ foo/bar
        # Which kind of look like diff lines but are definitely not
        elif line.startswith('--- ') and not in_diff: pass
        elif line.startswith('+++ ') and not in_diff:
            in_diff = True
        elif in_diff and line.startswith('+'):
            lines_added.append(line[1:])
        elif in_diff and line.startswith('-'):
            lines_removed.append(line[1:])

    assert mode is not None
    assert status is not None

    # Process symlinks
    symlink = None
    if mode == SYMLINK_MODE:
        symlink = Symlink(
            added=lines_added[0] if lines_added else None,
            removed=lines_removed[0] if lines_removed else None,
        )
        lines_added = []
        lines_removed = []

    return FileDiffStat(
        diff_line_filename,
        lines_added,
        lines_removed,
        status,
        symlink=symlink,
    )


def get_file_diff_stats_from_output(output):
    files = re.split('^diff --git ', output, flags=re.MULTILINE)
    assert not files[0].strip() or files[0].startswith('commit ')
    return map(_to_file_diff_stat, files[1:])
