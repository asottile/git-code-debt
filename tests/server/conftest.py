from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import mock
import pytest

import git_code_debt.server.app
from git_code_debt.generate import main
from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.client import Client


class GitCodeDebtServer(object):
    def __init__(self, client, sandbox):
        self.client = client
        self.sandbox = sandbox


@pytest.yield_fixture
def server(sandbox):
    app = git_code_debt.server.app.app
    with contextlib.nested(
        mock.patch.object(app, 'test_client_class', Client),
        # Making the app always debug so it throws exceptions
        mock.patch.object(
            type(app),
            'debug',
            mock.PropertyMock(return_value=True),
        ),
    ):
        with contextlib.nested(
            app.test_request_context(),
            app.test_client(),
            mock.patch.object(
                git_code_debt.server.app, 'database_path', sandbox.db_path,
            ),
        ) as (_, client, _):
            yield GitCodeDebtServer(client, sandbox)


@pytest.yield_fixture
def server_with_data(server, cloneable_with_commits):
    main([cloneable_with_commits.path, server.sandbox.db_path])
    yield auto_namedtuple(
        server=server,
        cloneable_with_commits=cloneable_with_commits,
    )
