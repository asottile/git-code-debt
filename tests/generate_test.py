from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import pytest

from git_code_debt.generate import increment_metric_values
from git_code_debt.generate import main
from git_code_debt.metric import Metric


def test_increment_metrics_first_time():
    metrics = collections.defaultdict(int)
    increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
    assert metrics == {'foo': 1, 'bar': 2}


def test_increment_metrics_already_there():
    metrics = collections.defaultdict(int, {'foo': 2, 'bar': 3})
    increment_metric_values(metrics, [Metric('foo', 1), Metric('bar', 2)])
    assert metrics == {'foo': 3, 'bar': 5}


@pytest.mark.integration
def test_generate_integration(sandbox, cloneable):
    main([cloneable, sandbox.db_path])


def get_metric_data_count(sandbox):
    with sandbox.db() as db:
        return db.execute('SELECT COUNT(*) FROM metric_data').fetchone()[0]


@pytest.mark.integration
def test_generate_integration_previous_data(sandbox, cloneable):
    main([cloneable, sandbox.db_path])
    before_data_count = get_metric_data_count(sandbox)
    main([cloneable, sandbox.db_path])
    after_data_count = get_metric_data_count(sandbox)
    assert before_data_count == after_data_count
