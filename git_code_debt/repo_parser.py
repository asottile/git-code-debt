
import collections
import contextlib
import shutil
import subprocess
import tempfile

from util.iter import chunk_iter

Commit = collections.namedtuple('Commit', ['sha', 'date', 'name'])

class RepoParser(object):

    def __init__(self, git_repo, ref):
        self.git_repo = git_repo
        self.ref = ref
        self.tempdir = None

    @contextlib.contextmanager
    def repo_checked_out(self):
        assert not self.tempdir
        self.tempdir = tempfile.mkdtemp(suffix='temp-repo')
        try:
            subprocess.call(
                ['git', 'clone', self.git_repo, self.tempdir],
                stdout=None,
            )
            subprocess.call(
                ['git', 'checkout', self.ref],
                cwd=self.tempdir,
                stdout=None,
            )
            yield
        finally:
            shutil.rmtree(self.tempdir)
            self.tempdir = None

    def get_commit_shas(self, since=None):
        assert self.tempdir

        cmd = ['git', 'log', self.ref,  '--topo-order', '--format=%H%n%at%n%cN']
        if since:
            cmd += ['--after={0}'.format(since)]

        output = subprocess.check_output(
            cmd,
            cwd=self.tempdir,
        )

        commits = []
        for sha, date, name in chunk_iter(output.splitlines(), 3):
            commits.append(Commit(sha, int(date), name))

        return commits
