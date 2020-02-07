import collections
import sqlite3
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

import flask


class Metric(NamedTuple):
    value: int
    date: int


class MetricInfo(NamedTuple):
    id: int
    description: str


def get_metric_ids(db: sqlite3.Connection) -> List[str]:
    query = 'SELECT name FROM metric_names WHERE has_data=1 ORDER BY name'
    res = db.execute(query).fetchall()
    return [name for name, in res]


def get_metric_info(db: sqlite3.Connection, metric_name: str) -> MetricInfo:
    query = 'SELECT id, description FROM metric_names WHERE name = ?'
    res = db.execute(query, (metric_name,)).fetchone()
    return MetricInfo(*res)


def get_latest_sha() -> Optional[str]:
    query = 'SELECT sha FROM metric_data ORDER BY timestamp DESC LIMIT 1'
    result = flask.g.db.execute(query).fetchone()

    # If there is no data result will be None
    return result[0] if result else None


def get_sha_for_date(date: int) -> Optional[str]:
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


def get_metrics_for_sha(sha: Optional[str]) -> Dict[str, int]:
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


def metrics_for_dates(metric_id: int, dates: Tuple[int, ...]) -> List[Metric]:
    def get_metric_for_timestamp(timestamp: int) -> Metric:
        result = flask.g.db.execute(
            'SELECT running_value, timestamp\n'
            'FROM metric_data\n'
            'WHERE metric_id = ? AND timestamp < ?\n'
            'ORDER BY timestamp DESC\n'
            'LIMIT 1\n',
            (metric_id, timestamp),
        ).fetchone()
        if result:
            return Metric(*result)
        else:
            return Metric(0, timestamp)

    return [get_metric_for_timestamp(date) for date in dates]


def get_first_data_timestamp(
        metric_name: str,
        db: Optional[sqlite3.Connection] = None,
) -> int:
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


def get_metric_changes(
        db: sqlite3.Connection,
        sha: str,
) -> List[Tuple[str, int]]:
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
        db: sqlite3.Connection,
        start_timestamp: int,
        end_timestamp: int,
        metric_id: int,
) -> List[Tuple[int, str, int]]:
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
            'WHERE',
            '    metric_data.timestamp >= ? AND',
            '    metric_data.timestamp < ? AND',
            '    metric_changes.metric_id = ?',
            'ORDER BY ABS(metric_changes.value) DESC',
            'LIMIT 50',
        )),
        (start_timestamp, end_timestamp, metric_id),
    ).fetchall()
