from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest

from git_code_debt.server import metric_config
from git_code_debt.server.presentation.commit_delta import CommitDelta


@pytest.yield_fixture
def patched_color_overrides():
    with mock.patch.object(
        metric_config, 'color_overrides', ['ColorOverrideMetric'],
    ):
        yield


@pytest.mark.usefixtures('patched_color_overrides')
def test_commit_delta_not_overriden():
    assert 'MyMetric' not in metric_config.color_overrides
    ret = CommitDelta.from_data('MyMetric', mock.sentinel.delta)
    assert ret == CommitDelta('MyMetric', '', mock.sentinel.delta)


@pytest.mark.usefixtures('patched_color_overrides')
def test_commit_delta_with_overrides():
    assert 'ColorOverrideMetric' in metric_config.color_overrides
    ret = CommitDelta.from_data('ColorOverrideMetric', mock.sentinel.delta)
    assert ret == CommitDelta(
        'ColorOverrideMetric', 'color-override', mock.sentinel.delta,
    )
