
import mock
import os.path
import pytest
import subprocess

from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import RepoParser
from testing.utilities.auto_namedtuple import auto_namedtuple


@pytest.mark.integration
def test_repo_checked_out(cloneable):
    repo_parser = RepoParser(cloneable)
    assert repo_parser.tempdir is None

    with repo_parser.repo_checked_out():
        assert repo_parser.tempdir is not None

        tempdir_path = repo_parser.tempdir
        assert os.path.exists(tempdir_path)
        assert os.path.exists(os.path.join(tempdir_path, '.git'))

    assert repo_parser.tempdir is None
    assert not os.path.exists(tempdir_path)


@pytest.yield_fixture
def checked_out_repo(cloneable_with_commits):
    repo_parser = RepoParser(cloneable_with_commits.path)
    with repo_parser.repo_checked_out():
        yield auto_namedtuple(
            repo_parser=repo_parser,
            cloneable_with_commits=cloneable_with_commits,
        )


@pytest.mark.integration
def test_get_commit_shas_all_of_them(checked_out_repo):
    with mock.patch.object(subprocess, 'check_output') as check_output_mock:
        commit = Commit('sha', 123, 'asottile')
        check_output_mock.return_value = '\n'.join(
            unicode(part) for part in commit
        ) + '\n'
        all_commits = checked_out_repo.repo_parser.get_commit_shas()
        assert all_commits == [commit]


@pytest.mark.integration
def test_get_commit_shas_after_date(checked_out_repo):
    with mock.patch.object(subprocess, 'check_output') as check_output_mock:
        previous_sha = '29d0d321f43950fd2aa1d1df9fc81dee0e9046b3'
        commit = Commit(previous_sha, 123, 'asottile')
        check_output_mock.return_value = '\n'.join(
            unicode(part) for part in commit
        ) + '\n'
        checked_out_repo.repo_parser.get_commit_shas(previous_sha)
        assert (
            '{0}..HEAD'.format(previous_sha) in
            check_output_mock.call_args[0][0]
        )


@pytest.mark.integration
def test_get_commits_since_commit_includes_that_commit(checked_out_repo):
    previous_sha = checked_out_repo.cloneable_with_commits.commits[0].sha
    all_commits = checked_out_repo.repo_parser.get_commit_shas(previous_sha)
    shas = [commit.sha for commit in all_commits]
    assert previous_sha in shas
    assert len(shas) == len(set(shas))


@pytest.mark.integration
def test_get_commit(checked_out_repo):
    # Smoke test
    first_commit = checked_out_repo.cloneable_with_commits.commits[0]
    sha = first_commit.sha
    ret = checked_out_repo.repo_parser.get_commit(sha)
    assert ret == first_commit
