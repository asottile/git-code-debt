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
