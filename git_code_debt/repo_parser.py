
import collections
import contextlib
import shutil
import subprocess
import tempfile

from util.backport_subprocess import backport_check_output
from util.iter import chunk_iter

# XXX: Python 2.6 compatibility
backport_check_output()

# TODO: remove name since we can't really do anything useful with it
Commit = collections.namedtuple('Commit', ['sha', 'date', 'name'])

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

    # TODO: rename this to get_commits
    def get_commit_shas(self, since_sha=None):
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """
        assert self.tempdir

        cmd = ['git', 'log', '--first-parent', '--reverse', '--format=%H%n%at%n%cN']
        if since_sha:
            cmd.append('{0}..master'.format(since_sha))
        else:
            cmd.append('master')

        output = subprocess.check_output(
            cmd,
            cwd=self.tempdir,
        )

        commits = []
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

    def get_commit_diff(self, previous_sha, sha):
        assert self.tempdir
        output = subprocess.check_output(
            ['git', 'diff', previous_sha, sha],
            cwd=self.tempdir,
        )
        return output


