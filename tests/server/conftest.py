# pylint:disable=redefined-outer-name
from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib

import mock
import pytest

from git_code_debt.generate import main
from git_code_debt.server.app import app
from git_code_debt.server.app import AppContext
from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.client import Client


class GitCodeDebtServer(object):
    def __init__(self, client, sandbox):
        self.client = client
        self.sandbox = sandbox


@contextlib.contextmanager
def _patch_app_with_client(application):
    with mock.patch.object(application, 'test_client_class', Client):
        # Make the app always debug so it throws exceptions
        with mock.patch.object(
            type(application), 'debug', mock.PropertyMock(return_value=True),
        ):
            yield


@contextlib.contextmanager
def _in_testing_app_context(application):
    with application.test_request_context():
        with application.test_client() as client:
            yield client


@pytest.yield_fixture
def server(sandbox):
    with _patch_app_with_client(app):
        with _in_testing_app_context(app) as client:
            with mock.patch.object(
                AppContext, 'database_path', sandbox.db_path,
            ):
                yield GitCodeDebtServer(client, sandbox)


@pytest.yield_fixture
def server_with_data(server, cloneable_with_commits):
    main([cloneable_with_commits.path, server.sandbox.db_path])
    yield auto_namedtuple(
        server=server,
        cloneable_with_commits=cloneable_with_commits,
    )
