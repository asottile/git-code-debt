import contextlib
import shutil
import subprocess
import tempfile
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Optional

from git_code_debt.util.iter import chunk_iter
from git_code_debt.util.subprocess import cmd_output
from git_code_debt.util.subprocess import cmd_output_b


class Commit(NamedTuple):
    sha: str
    date: int


BLANK_COMMIT = Commit('0' * 40, 0)

COMMIT_FORMAT = '--format=%H%n%ct'


class RepoParser:

    def __init__(self, git_repo: str) -> None:
        self.git_repo = git_repo
        self.tempdir: Optional[str] = None

    @contextlib.contextmanager
    def repo_checked_out(self) -> Generator[None, None, None]:
        assert not self.tempdir
        self.tempdir = tempfile.mkdtemp(suffix='temp-repo')
        try:
            subprocess.check_call((
                'git', 'clone',
                '--no-checkout', '--quiet', '--shared',
                self.git_repo, self.tempdir,
            ))
            yield
        finally:
            shutil.rmtree(self.tempdir)
            self.tempdir = None

    def get_commit(self, sha: str) -> Commit:
        output = cmd_output(
            'git', 'show', COMMIT_FORMAT, sha, cwd=self.tempdir,
        )
        sha, date = output.splitlines()[:2]

        return Commit(sha, int(date))

    def get_commits(self, since_sha: Optional[str] = None) -> List[Commit]:
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """
        assert self.tempdir

        cmd = ['git', 'log', '--first-parent', '--reverse', COMMIT_FORMAT]
        if since_sha:
            commits = [self.get_commit(since_sha)]
            cmd.append(f'{since_sha}..HEAD')
        else:
            commits = []
            cmd.append('HEAD')

        output = cmd_output(*cmd, cwd=self.tempdir)

        for sha, date in chunk_iter(output.splitlines(), 2):
            commits.append(Commit(sha, int(date)))

        return commits

    def get_original_commit(self, sha: str) -> bytes:
        assert self.tempdir
        return cmd_output_b('git', 'show', sha, cwd=self.tempdir)

    def get_commit_diff(self, previous_sha: str, sha: str) -> bytes:
        assert self.tempdir
        return cmd_output_b(
            'git', 'diff', previous_sha, sha, '--no-renames',
            cwd=self.tempdir,
        )
