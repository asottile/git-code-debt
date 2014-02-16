
import contextlib
import mock
import pytest

import git_code_debt_server.app
from git_code_debt.generate import main
from testing.utilities.client import Client


class GitCodeDebtServer(object):
    def __init__(self, client):
        self.client = client


@pytest.yield_fixture
def server():
    app = git_code_debt_server.app.app
    with contextlib.nested(
        mock.patch.object(app, 'test_client_class', Client),
        # Making the app always debug so it throwse exceptions
        mock.patch.object(
            type(app),
            'debug',
            mock.PropertyMock(return_value=True),
        ),
    ):
        with contextlib.nested(
            app.test_request_context(), app.test_client()
        ) as (_, client):
            yield GitCodeDebtServer(client)


class GitCodeDebtServerWithData(GitCodeDebtServer):
    def __init__(self, base_server, sandbox):
        super(GitCodeDebtServerWithData, self).__init__(base_server.client)
        self.sandbox = sandbox


@pytest.yield_fixture
def server_with_data(server, sandbox):
    main(['.', sandbox.db_path])
    with mock.patch.object(
        git_code_debt_server.app, 'database_path', sandbox.db_path,
    ):
        yield GitCodeDebtServerWithData(server, sandbox)
