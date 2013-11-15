
import mock
import os.path
import subprocess
import testify as T

from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import RepoParser

@T.suite('integration')
class RepoParserRepoCheckedOutTest(T.TestCase):

    def get_repo_parser(self):
        return RepoParser(
            'git@github.com:asottile/git-code-debt',
        )

    def test_repo_checked_out(self):
        repo_parser = self.get_repo_parser()
        T.assert_is(repo_parser.tempdir, None)

        with repo_parser.repo_checked_out():
            T.assert_is_not(repo_parser.tempdir, None)

            tempdir_path = repo_parser.tempdir
            T.assert_equal(os.path.exists(tempdir_path), True)
            T.assert_equal(
                os.path.exists(os.path.join(tempdir_path, '.git')),
                True,
            )

        T.assert_is(repo_parser.tempdir, None)
        T.assert_equal(os.path.exists(tempdir_path), False)

@T.suite('integration')
class RepoParserTest(T.TestCase):

    @T.class_setup_teardown
    def check_out_repo(self):
        self.repo_parser = RepoParser('git@github.com:asottile/git-code-debt')
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
            check_output_mock.return_value = ''
            after_time = 12345
            all_commits = self.repo_parser.get_commit_shas(12345)
            T.assert_equal(all_commits, [])
            T.assert_in(
                '{0}..master'.format(after_time),
                check_output_mock.call_args[0][0]
            )
