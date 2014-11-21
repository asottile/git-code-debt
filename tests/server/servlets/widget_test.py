from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib

import flask
import pyquery
import staticconf.testing

from git_code_debt.server.metric_config import CONFIG_NAMESPACE
from testing.assertions.response import assert_no_response_errors
from tests import file_diff_stat_test


def test_widget_frame_loads(server):
    response = server.client.get(flask.url_for('widget.frame'))
    assert_no_response_errors(response)
    assert response.pq.find('script')


@contextlib.contextmanager
def metrics_enabled(widget_metrics):
    config = {
        'Groups': [],
        'CommitLinks': [],
        'ColorOverrides': [],
        'WidgetMetrics': widget_metrics,
    }
    with staticconf.testing.MockConfiguration(
        config,
        flatten=False,
        namespace=CONFIG_NAMESPACE,
    ):
        yield


def test_widget_data(server):
    with metrics_enabled({'TotalLinesOfCode': {}}):
        response = server.client.post(
            flask.url_for('widget.data'),
            data={
                'diff': file_diff_stat_test.SAMPLE_OUTPUT
            }
        )
    response_pq = pyquery.PyQuery(response.json['metrics'])
    assert 'TotalLinesOfCode 1' in response_pq.text()
    # Should not find any metrics with no data
    assert not response_pq.find('.metric-none')
    # Should not have metrics we didn't specify
    assert 'TotalLinesOfCode_Text' not in response_pq.text()


def test_widget_data_multiple_values(server):
    with metrics_enabled(
        {'TotalLinesOfCode': {}, 'TotalLinesOfCode_Text': {}}
    ):
        response = server.client.post(
            flask.url_for('widget.data'),
            data={
                'diff': file_diff_stat_test.SAMPLE_OUTPUT,
            },
        )
    response_pq = pyquery.PyQuery(response.json['metrics'])
    assert 'TotalLinesOfCode_Text' in response_pq.text()
