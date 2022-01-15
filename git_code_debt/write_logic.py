from __future__ import annotations

import sqlite3

from git_code_debt.metric import Metric
from git_code_debt.repo_parser import Commit


def insert_metric_values(
        db: sqlite3.Connection,
        metric_values: dict[int, int],
        has_data: dict[int, bool],
        commit: Commit,
) -> None:
    values = [
        (commit.sha, metric_id, commit.date, value)
        for metric_id, value in metric_values.items()
        if has_data[metric_id]
    ]
    db.executemany(
        'INSERT INTO metric_data (sha, metric_id, timestamp, running_value)\n'
        'VALUES (?, ?, ?, ?)\n',
        values,
    )


def insert_metric_changes(
        db: sqlite3.Connection,
        metrics: tuple[Metric, ...],
        metric_mapping: dict[str, int],
        commit: Commit,
) -> None:
    """Insert into the metric_changes tables.

    :param metrics: `list` of `Metric` objects
    :param dict metric_mapping: Maps metric names to ids
    :param Commit commit:
    """
    values = [
        [commit.sha, metric_mapping[metric.name], metric.value]
        for metric in metrics
        if metric.value != 0
    ]
    db.executemany(
        'INSERT INTO metric_changes (sha, metric_id, value) VALUES (?, ?, ?)',
        values,
    )
