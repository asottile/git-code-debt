from __future__ import absolute_import
from __future__ import unicode_literals

import flask

from testing.assertions.response import assert_no_response_errors


def test_it_loads(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'commit.show',
        sha=server_with_data.cloneable_with_commits.commits[3].sha,
    ))
    assert_no_response_errors(resp)
    import_row = resp.pq.find('th:contains("PythonImportCount")').parent()
    assert import_row.find('td').text() == '2'


def test_it_loads_for_first_commit(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'commit.show',
        sha=server_with_data.cloneable_with_commits.commits[0].sha,
    ))
    assert_no_response_errors(resp)
