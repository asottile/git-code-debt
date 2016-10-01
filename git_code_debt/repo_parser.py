from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import contextlib
import shutil
import subprocess
import tempfile

from git_code_debt.util.iter import chunk_iter
from git_code_debt.util.subprocess import cmd_output


Commit = collections.namedtuple('Commit', ('sha', 'date'))
Commit.blank = Commit('0' * 40, 0)

COMMIT_FORMAT = '--format=%H%n%ct'


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
                (
                    'git', 'clone',
                    '--no-checkout', '--shared',
                    self.git_repo, self.tempdir,
                ),
                stdout=None,
            )
            yield
        finally:
            shutil.rmtree(self.tempdir)
            self.tempdir = None

    def get_commit(self, sha):
        output = cmd_output(
            'git', 'show', COMMIT_FORMAT, sha,
            cwd=self.tempdir,
        )
        sha, date = output.splitlines()[:2]

        return Commit(sha, int(date))

    def get_commits(self, since_sha=None):
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """
        assert self.tempdir

        cmd = ['git', 'log', '--first-parent', '--reverse', COMMIT_FORMAT]
        if since_sha:
            commits = [self.get_commit(since_sha)]
            cmd.append('{0}..HEAD'.format(since_sha))
        else:
            commits = []
            cmd.append('HEAD')

        output = cmd_output(*cmd, cwd=self.tempdir)

        for sha, date in chunk_iter(output.splitlines(), 2):
            commits.append(Commit(sha, int(date)))

        return commits

    def get_original_commit(self, sha):
        assert self.tempdir
        output = cmd_output(
            'git', 'show', sha, cwd=self.tempdir, encoding=None,
        )
        return output

    def get_commit_diff(self, previous_sha, sha):
        assert self.tempdir
        output = cmd_output(
            'git', 'diff', previous_sha, sha, '--no-renames',
            cwd=self.tempdir, encoding=None,
        )
        return output
