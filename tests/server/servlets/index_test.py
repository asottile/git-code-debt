import flask

from git_code_debt.server.servlets.index import Metric
from testing.assertions.response import assert_no_response_errors


def _test_it_loads(server):
    response = server.client.get(flask.url_for('index.show'))
    assert_no_response_errors(response)
    # Should have a nonzero number of links to things
    assert response.pq.find('a[href]')
    return response


def test_it_loads_no_data(server):
    _test_it_loads(server)


def test_it_loads_with_data(server_with_data):
    resp = _test_it_loads(server_with_data.server)
    assert 'CurseWords' not in resp.text


def test_metric_classname_overriden():
    metric = Metric('metric', True, 0, (), '')
    assert metric.classname == 'color-override'


def test_metric_classname_normal():
    metric = Metric('metric', False, 0, (), '')
    assert metric.classname == ''
