
import collections
import contextlib
import shutil
import subprocess
import tempfile

from git_code_debt_util.backport_subprocess import backport_check_output
from git_code_debt_util.iter import chunk_iter

# XXX: Python 2.6 compatibility
backport_check_output()

# TODO: remove name since we can't really do anything useful with it
Commit = collections.namedtuple('Commit', ['sha', 'date', 'name'])

COMMIT_FORMAT = '--format=%H%n%at%n%cN'

class RepoParser(object):

    def __init__(self, git_repo):
        self.git_repo = git_repo
        self.tempdir = None

    @contextlib.contextmanager
    def repo_checked_out(self):
        assert not self.tempdir
        self.tempdir = tempfile.mkdtemp(suffix='temp-repo')
        try:
            subprocess.check_call(
                ['git', 'clone', self.git_repo, self.tempdir],
                stdout=None,
            )
            yield
        finally:
            shutil.rmtree(self.tempdir)
            self.tempdir = None

    def get_commit(self, sha):
        output = subprocess.check_output(
            ['git', 'show', COMMIT_FORMAT, sha],
            cwd=self.tempdir,
        )
        sha, date, name, = output.splitlines()[:3]

        return Commit(sha, int(date), name)

    # TODO: rename this to get_commits
    def get_commit_shas(self, since_sha=None):
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """
        assert self.tempdir

        cmd = ['git', 'log', '--oneline', '--reverse', COMMIT_FORMAT]
        if since_sha:
            commits = [self.get_commit(since_sha)]
            cmd.append('{0}..HEAD'.format(since_sha))
        else:
            commits = []
            cmd.append('HEAD')

        output = subprocess.check_output(
            cmd,
            cwd=self.tempdir,
        )

        for sha, date, name in chunk_iter(output.splitlines(), 3):
            commits.append(Commit(sha, int(date), name))

        return commits

    def get_original_commit(self, sha):
        assert self.tempdir
        output = subprocess.check_output(
            ['git', 'show', sha],
            cwd=self.tempdir,
        )
        return output

    def get_original_diff_stat(self, sha):
        assert self.tempdir
        return subprocess.check_output(
            ['git', 'show', sha, '--oneline', '--stat'],
            cwd=self.tempdir
        )

    def get_commit_diff(self, previous_sha, sha):
        assert self.tempdir
        output = subprocess.check_output(
            ['git', 'diff', previous_sha, sha],
            cwd=self.tempdir,
        )
        return output

    def get_commit_diff_stat(self, previous_sha, sha):
        assert self.tempdir
        return subprocess.check_output(
            ['git', 'diff', previous_sha, sha, '--stat'],
            cwd=self.tempdir,
        )
