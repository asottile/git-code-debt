from __future__ import annotations

import os.path
from unittest import mock

import pytest

from git_code_debt import repo_parser
from testing.utilities.auto_namedtuple import auto_namedtuple


def test_repo_checked_out(cloneable):
    parser = repo_parser.RepoParser(cloneable)
    assert parser.tempdir is None

    with parser.repo_checked_out():
        assert parser.tempdir is not None

        tempdir_path = parser.tempdir
        assert os.path.exists(tempdir_path)
        assert os.path.exists(os.path.join(tempdir_path, '.git'))

    assert parser.tempdir is None
    assert not os.path.exists(tempdir_path)


@pytest.fixture
def checked_out_repo(cloneable_with_commits):
    parser = repo_parser.RepoParser(cloneable_with_commits.path)
    with parser.repo_checked_out():
        yield auto_namedtuple(
            repo_parser=parser,
            cloneable_with_commits=cloneable_with_commits,
        )


def test_get_commits_all_of_them(checked_out_repo):
    with mock.patch.object(repo_parser, 'cmd_output') as cmd_output_mock:
        commit = repo_parser.Commit('sha', 123)
        cmd_output_mock.return_value = '\n'.join(
            str(part) for part in commit
        ) + '\n'
        all_commits = checked_out_repo.repo_parser.get_commits()
        assert all_commits == [commit]


def test_get_commits_after_date(checked_out_repo):
    with mock.patch.object(repo_parser, 'cmd_output') as cmd_output_mock:
        previous_sha = '29d0d321f43950fd2aa1d1df9fc81dee0e9046b3'
        commit = repo_parser.Commit(previous_sha, 123)
        cmd_output_mock.return_value = '\n'.join(
            str(part) for part in commit
        ) + '\n'
        checked_out_repo.repo_parser.get_commits(previous_sha)
        assert (
            f'{previous_sha}..HEAD' in
            cmd_output_mock.call_args[0]
        )


def test_get_commits_since_commit_includes_that_commit(checked_out_repo):
    previous_sha = checked_out_repo.cloneable_with_commits.commits[0].sha
    all_commits = checked_out_repo.repo_parser.get_commits(previous_sha)
    shas = [commit.sha for commit in all_commits]
    assert previous_sha in shas
    assert len(shas) == len(set(shas))


def test_get_commit(checked_out_repo):
    # Smoke test
    first_commit = checked_out_repo.cloneable_with_commits.commits[0]
    sha = first_commit.sha
    ret = checked_out_repo.repo_parser.get_commit(sha)
    assert ret == first_commit
