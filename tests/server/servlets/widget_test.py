from __future__ import absolute_import
from __future__ import unicode_literals

import flask
import pyquery

from testing.assertions.response import assert_no_response_errors
from tests import file_diff_stat_test


def test_widget_frame_loads(server):
    response = server.client.get(flask.url_for('widget.frame'))
    assert_no_response_errors(response)
    assert response.pq.find('script')


def test_widget_data(server):
    response = server.client.post(
        flask.url_for('widget.data'),
        data={
            'metric_names[]': ['TotalLinesOfCode'],
            'diff': file_diff_stat_test.SAMPLE_OUTPUT
        }
    )
    response_pq = pyquery.PyQuery(response.json['metrics'])
    assert 'TotalLinesOfCode 1' in response_pq.text()
    # Should not find any metrics with no data
    assert not response_pq.find('.metric-none')
    # Should not have metrics we didn't specify
    assert 'TotalLinesOfCode_Text' not in response_pq.text()
