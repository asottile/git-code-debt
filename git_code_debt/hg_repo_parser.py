import contextlib
import subprocess
import tempfile
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Optional

from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import RepoParser
from git_code_debt.util.iter import chunk_iter
from git_code_debt.util.subprocess import cmd_output
from git_code_debt.util.subprocess import cmd_output_b


TEMPLATE = 'commit {node}\nAuthor: {author}\nDate:   {date|date}\n\n{indent(desc, \"    \")}\n\n'


class HgRepoParser(RepoParser):

    def __init__(self, repo: str) -> None:
        self.repo = repo
        self.tempdir: Optional[str] = None

    @contextlib.contextmanager
    def repo_checked_out(self) -> Generator[None, None, None]:
        assert not self.tempdir
        with tempfile.TemporaryDirectory(suffix='temp-repo') as self.tempdir:
            try:
                subprocess.check_call((
                    'hg', 'clone',
                    '--noupdate', '--quiet',
                    self.repo, self.tempdir,
                ))
                yield
            finally:
                self.tempdir = None

    def get_commit(self, sha: str) -> Commit:
        output = cmd_output(
            'hg', 'log', '--template={node}\n{word(0, date, \".\")}\n', '--rev', sha,
            cwd=self.tempdir,
        )
        sha, date = output.splitlines()[:2]

        # hg's default date formate is <utc timestamp>.<offset> so we just
        # chop off the offset since we don't want/need it.
        return Commit(sha, int(date))

    def get_commits(self, since_sha: Optional[str] = None) -> List[Commit]:
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """
        assert self.tempdir

        commits = []

        cmd = ['hg', 'log', '--template={node}\n{word(0, date, \".\")}\n']
        if since_sha:
            cmd.extend(['--rev', f'reverse({since_sha}:. and branch(.))'])

        output = cmd_output(*cmd, cwd=self.tempdir)
        for sha, date in chunk_iter(output.splitlines(), 2):
            commits.append(Commit(sha, int(date)))

        return commits

    def get_original_commit(self, sha: str) -> bytes:
        assert self.tempdir
        return cmd_output_b(
            'hg', 'log', '--git', '--patch', f'--template={TEMPLATE}',
            '--rev', sha, cwd=self.tempdir,
        )

    def get_commit_diff(self, previous_sha: str, sha: str) -> bytes:
        assert self.tempdir
        return cmd_output_b(
            'hg', 'diff', '--git', '--from', previous_sha, '--to', sha,
            cwd=self.tempdir,
        )
