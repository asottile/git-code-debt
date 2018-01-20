from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from git_code_debt.server.presentation.commit_delta import CommitDelta


def test_commit_delta_not_overriden():
    overrides = {'OtherMetric'}
    ret = CommitDelta.from_data('MyMetric', mock.sentinel.delta, overrides)
    assert ret == CommitDelta('MyMetric', '', mock.sentinel.delta)


def test_commit_delta_with_overrides():
    overrides = {'OtherMetric'}
    ret = CommitDelta.from_data('OtherMetric', mock.sentinel.delta, overrides)
    assert ret == CommitDelta(
        'OtherMetric', 'color-override', mock.sentinel.delta,
    )
