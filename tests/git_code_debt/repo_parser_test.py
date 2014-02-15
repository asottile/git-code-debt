
import mock
import os.path
import subprocess
import testify as T

from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import RepoParser
from testing.base_classes.test import test

@T.suite('integration')
@test
def test_repo_checked_out():
    repo_parser = RepoParser('.')
    T.assert_is(repo_parser.tempdir, None)

    with repo_parser.repo_checked_out():
        T.assert_is_not(repo_parser.tempdir, None)

        tempdir_path = repo_parser.tempdir
        T.assert_equal(os.path.exists(tempdir_path), True)
        T.assert_is(
            os.path.exists(os.path.join(tempdir_path, '.git')),
            True,
        )

    T.assert_is(repo_parser.tempdir, None)
    T.assert_is(os.path.exists(tempdir_path), False)


@T.suite('integration')
class RepoParserTest(T.TestCase):
    @T.class_setup_teardown
    def check_out_repo(self):
        self.repo_parser = RepoParser('.')
        with self.repo_parser.repo_checked_out():
            yield

    def test_get_commit_shas_all_of_them(self):
        with mock.patch.object(subprocess, 'check_output') as check_output_mock:
            commit = Commit('sha', 123, 'asottile')
            check_output_mock.return_value = '\n'.join(unicode(part) for part in commit) + '\n'
            all_commits = self.repo_parser.get_commit_shas()
            T.assert_equal(all_commits, [commit])

    def test_get_commit_shas_after_date(self):
        with mock.patch.object(subprocess, 'check_output') as check_output_mock:
            previous_sha = '29d0d321f43950fd2aa1d1df9fc81dee0e9046b3'
            commit = Commit(previous_sha, 123, 'asottile')
            check_output_mock.return_value = '\n'.join(unicode(part) for part in commit) + '\n'
            self.repo_parser.get_commit_shas(previous_sha)
            T.assert_in(
                '{0}..HEAD'.format(previous_sha),
                check_output_mock.call_args[0][0]
            )

    def test_get_commits_since_commit_includes_that_commit(self):
        previous_sha = '29d0d321f43950fd2aa1d1df9fc81dee0e9046b3'
        all_commits = self.repo_parser.get_commit_shas(previous_sha)
        shas = [commit.sha for commit in all_commits]
        T.assert_in(previous_sha, shas)
        T.assert_equal(len(shas), len(set(shas)))

    def test_get_commit(self):
        # Smoke test
        sha = '29d0d321f43950fd2aa1d1df9fc81dee0e9046b3'
        ret = self.repo_parser.get_commit(sha)
        T.assert_equal(ret, Commit(sha, 1385346958, 'Anthony Sottile'))
