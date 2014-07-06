from __future__ import absolute_import
from __future__ import unicode_literals


def get_metric_mapping(db):
    """Gets a mapping from metric_name to metric_id."""
    results = db.execute('SELECT name, id FROM metric_names').fetchall()
    return dict(results)


def get_previous_sha(db, repo):
    """Gets the latest inserted SHA for a specific repo."""
    result = db.execute(
        """
        SELECT
            sha
        FROM metric_data
        WHERE repo = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        [repo]
    ).fetchone()

    return result[0] if result else None


def get_metric_values(db, commit):
    """Gets the metric values from a specific commit.

    Args:
        db - Database object
        commit - a Commit object with a sha property
    """
    results = db.execute(
        """
        SELECT
            metric_names.name,
            running_value
        FROM metric_data
        INNER JOIN metric_names ON
            metric_names.id = metric_data.metric_id
        WHERE sha = ?
        """,
        [commit.sha],
    )
    return dict(results)


def insert_metric_values(db, metric_values, metric_mapping, repo, commit):
    for metric_name, value in metric_values.items():
        metric_id = metric_mapping[metric_name]
        db.execute(
            """
            INSERT INTO metric_data
            (repo, sha, metric_id, timestamp, running_value)
            VALUES (?, ?, ?, ?, ?)
            """,
            [repo, commit.sha, metric_id, commit.date, value],
        )
