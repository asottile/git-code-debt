from __future__ import absolute_import
from __future__ import unicode_literals


def insert_metric_ids(db, metric_ids):
    values = [[x] for x in metric_ids]
    db.executemany("INSERT INTO metric_names ('name') VALUES (?)", values)


def insert_metric_values(db, metric_values, metric_mapping, commit):
    values = [
        [commit.sha, metric_mapping[metric_name], commit.date, value]
        for metric_name, value in metric_values.items()
    ]
    db.executemany(
        'INSERT INTO metric_data\n'
        '(sha, metric_id, timestamp, running_value)\n'
        'VALUES (?, ?, ?, ?)\n',
        values,
    )


def insert_metric_changes(db, metrics, metric_mapping, commit):
    """Insert into the metric_changes tables.

    :param metrics: `list` of `Metric` objects
    :param dict metric_mapping: Maps metric names to ids
    :param Commit commit:
    """
    values = [
        [commit.sha, metric_mapping[metric.name], metric.value]
        for metric in metrics
        # Sparse table, ignore zero.
        if metric.value != 0
    ]
    db.executemany(
        'INSERT INTO metric_changes (sha, metric_id, value) VALUES (?, ?, ?)',
        values,
    )
