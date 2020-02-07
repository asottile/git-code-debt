import enum
import os.path
import re
from typing import List
from typing import NamedTuple
from typing import Optional


Status = enum.Enum('Status', 'ADDED DELETED ALREADY_EXISTING')
SpecialFileType = enum.Enum('SpecialFileType', 'SUBMODULE SYMLINK BINARY')


class SpecialFile(NamedTuple):
    file_type: SpecialFileType
    added: Optional[bytes]
    removed: Optional[bytes]


class FileDiffStat(NamedTuple):
    path: bytes
    lines_added: List[bytes]
    lines_removed: List[bytes]
    status: Status
    special_file: Optional[SpecialFile] = None

    @property
    def extension(self) -> bytes:
        return os.path.splitext(self.path)[1]

    @property
    def filename(self) -> bytes:
        return os.path.split(self.path)[1]


SUBMODULE_MODE = b'160000'
SYMLINK_MODE = b'120000'


def _to_file_diff_stat(file_diff: bytes) -> FileDiffStat:
    lines = file_diff.split(b'\n')
    diff_line_filename = lines[0].split()[-1].lstrip(b'b').lstrip(b'/')
    is_binary = False
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
        if line.startswith(b'new file mode '):
            assert status is None
            assert mode is None
            status = Status.ADDED
            mode = line.split()[-1]
        elif line.startswith(b'deleted file mode '):
            assert status is None
            assert mode is None
            status = Status.DELETED
            mode = line.split()[-1]
        elif line.startswith(b'new mode '):
            assert status is None
            assert mode is None
            status = Status.ALREADY_EXISTING
            mode = line.split()[-1]
        elif line.startswith(b'index') and len(line.split()) == 3:
            assert status is None
            assert mode is None
            status = Status.ALREADY_EXISTING
            mode = line.split()[-1]
        elif line.startswith(b'Binary files'):
            is_binary = True
        # A diff contains lines that look like:
        # --- foo/bar
        # +++ foo/bar
        # Which kind of look like diff lines but are definitely not
        elif line.startswith(b'--- ') and not in_diff:
            pass
        elif line.startswith(b'+++ ') and not in_diff:
            in_diff = True
        elif in_diff and line.startswith(b'+'):
            lines_added.append(line[1:])
        elif in_diff and line.startswith(b'-'):
            lines_removed.append(line[1:])

    assert mode is not None
    assert status is not None

    # Process symlinks and submodules
    special_file = None
    if mode == SUBMODULE_MODE:
        special_file = SpecialFile(
            file_type=SpecialFileType.SUBMODULE,
            added=lines_added[0].split()[-1] if lines_added else None,
            removed=lines_removed[0].split()[-1] if lines_removed else None,
        )
        lines_added = []
        lines_removed = []
    elif mode == SYMLINK_MODE:
        special_file = SpecialFile(
            file_type=SpecialFileType.SYMLINK,
            added=lines_added[0] if lines_added else None,
            removed=lines_removed[0] if lines_removed else None,
        )
        lines_added = []
        lines_removed = []
    elif is_binary:
        special_file = SpecialFile(
            file_type=SpecialFileType.BINARY,
            added=diff_line_filename if status is not Status.DELETED else None,
            removed=diff_line_filename if status is not Status.ADDED else None,
        )

    return FileDiffStat(
        diff_line_filename,
        lines_added,
        lines_removed,
        status,
        special_file=special_file,
    )


GIT_DIFF_RE = re.compile(b'^diff --git', flags=re.MULTILINE)


def get_file_diff_stats_from_output(output: bytes) -> List[FileDiffStat]:
    files = GIT_DIFF_RE.split(output)
    assert not files[0].strip() or files[0].startswith(b'commit ')
    return [_to_file_diff_stat(file_diff) for file_diff in files[1:]]
