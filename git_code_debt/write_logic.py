from __future__ import absolute_import
from __future__ import unicode_literals


def insert_metric_ids(db, metric_ids):
    for metric_id in metric_ids:
        db.execute(
            "INSERT INTO metric_names ('name') VALUES (?)", [metric_id],
        )


def insert_metric_values(db, metric_values, metric_mapping, commit):
    for metric_name, value in metric_values.items():
        metric_id = metric_mapping[metric_name]
        db.execute(
            '\n'.join((
                'INSERT INTO metric_data',
                '(sha, metric_id, timestamp, running_value)',
                'VALUES (?, ?, ?, ?)',
            )),
            [commit.sha, metric_id, commit.date, value],
        )


def insert_metric_changes(db, metrics, metric_mapping, commit):
    """Insert into the metric_changes tables.

    :param metrics: `list` of `Metric` objects
    :param dict metric_mapping: Maps metric names to ids
    :param Commit commit:
    """
    for metric in metrics:
        # Sparse table, ignore zero.
        if metric.value == 0:
            continue

        metric_id = metric_mapping[metric.name]
        db.execute(
            '\n'.join((
                'INSERT INTO metric_changes',
                '(sha, metric_id, value)',
                'VALUES (?, ?, ?)',
            )),
            [commit.sha, metric_id, metric.value],
        )
