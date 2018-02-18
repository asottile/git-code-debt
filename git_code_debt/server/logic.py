from __future__ import absolute_import
from __future__ import unicode_literals

import collections

import flask


Metric = collections.namedtuple('Metric', ('name', 'value', 'date'))


def get_metric_ids(db):
    query = 'SELECT name FROM metric_names WHERE has_data=1 ORDER BY name'
    res = db.execute(query).fetchall()
    return [name for name, in res]


def get_latest_sha():
    result = flask.g.db.execute(
        'SELECT sha FROM metric_data ORDER BY timestamp DESC LIMIT 1',
    ).fetchone()

    # If there is no data result will be None
    return result[0] if result else None


def get_sha_for_date(date):
    result = flask.g.db.execute(
        '\n'.join((
            'SELECT',
            '    sha',
            'FROM metric_data',
            'WHERE',
            '    timestamp <= ?',
            'ORDER BY timestamp DESC',
            'LIMIT 1',
        )),
        [date],
    ).fetchone()

    # If the date is too far in the past (before data) there won't be a result
    return result[0] if result else None


def get_metrics_for_sha(sha):
    # For no sha, we default all metrics to 0
    if not sha:
        return collections.defaultdict(int)

    result = flask.g.db.execute(
        'SELECT\n'
        '    metric_names.name,\n'
        '    metric_data.running_value\n'
        'FROM metric_data\n'
        'INNER JOIN metric_names ON\n'
        '    metric_names.id = metric_data.metric_id AND\n'
        '    metric_names.has_data = 1\n'
        'WHERE\n'
        '    metric_data.sha = ?\n',
        [sha],
    ).fetchall()

    return collections.defaultdict(int, result)


def metrics_for_dates(metric_name, dates):
    def get_metric_for_timestamp(timestamp):
        result = flask.g.db.execute(
            '\n'.join((
                'SELECT',
                '    running_value,',
                '    timestamp',
                'FROM metric_data',
                'INNER JOIN metric_names ON',
                '    metric_names.id = metric_data.metric_id',
                'WHERE',
                '    metric_names.name = ? AND',
                '    timestamp < ?',
                'ORDER BY timestamp DESC',
                'LIMIT 1',
            )),
            [metric_name, timestamp],
        ).fetchone()
        if result:
            return Metric(metric_name, *result)
        else:
            return Metric(metric_name, 0, timestamp)

    return [get_metric_for_timestamp(date) for date in dates]


def get_first_data_timestamp(metric_name, db=None):
    db = db or flask.g.db

    # Find the first change for that metric
    first_timestamp = db.execute(
        'SELECT timestamp\n'
        'FROM metric_data\n'
        'INNER JOIN metric_names ON metric_names.id = metric_data.metric_id\n'
        'WHERE metric_names.name = ?\n'
        'ORDER BY metric_data.ROWID ASC\n'
        'LIMIT 1\n',
        (metric_name,),
    ).fetchone()
    if not first_timestamp:
        return 0
    else:
        return first_timestamp[0]


def get_metric_changes(db, sha):
    return db.execute(
        '\n'.join((
            'SELECT',
            '    metric_names.name,',
            '    metric_changes.value',
            'FROM metric_changes',
            'INNER JOIN metric_names',
            '    ON metric_changes.metric_id = metric_names.id',
            'WHERE metric_changes.sha = ?',
        )),
        [sha],
    ).fetchall()


def get_major_changes_for_metric(
        db, start_timestamp, end_timestamp, metric_name,
):
    return db.execute(
        '\n'.join((
            'SELECT',
            '    metric_data.timestamp,',
            '    metric_data.sha,',
            '    metric_changes.value',
            'FROM metric_changes',
            'INNER JOIN metric_data ON',
            '    metric_changes.sha = metric_data.sha AND',
            '    metric_changes.metric_id = metric_data.metric_id',
            'INNER JOIN metric_names ON',
            '    metric_changes.metric_id = metric_names.id',
            'WHERE',
            '    metric_data.timestamp >= ? AND',
            '    metric_data.timestamp < ? AND',
            '    metric_names.name = ?',
            'ORDER BY ABS(metric_changes.value) DESC',
            'LIMIT 50',
        )),
        [start_timestamp, end_timestamp, metric_name],
    ).fetchall()
