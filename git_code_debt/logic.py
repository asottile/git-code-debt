from __future__ import absolute_import
from __future__ import unicode_literals


def get_metric_mapping(db):
    """Gets a mapping from metric_name to metric_id."""
    results = db.execute('SELECT name, id FROM metric_names').fetchall()
    return dict(results)


def get_metric_has_data(db):
    res = db.execute('SELECT id, has_data FROM metric_names').fetchall()
    return {k: bool(v) for k, v in res}


def get_previous_sha(db):
    """Gets the latest inserted SHA."""
    result = db.execute(
        # Use ROWID as a free, auto-incrementing, primary key.
        'SELECT sha FROM metric_data ORDER BY ROWID DESC LIMIT 1',
    ).fetchone()

    return result[0] if result else None


def get_metric_values(db, sha):
    """Gets the metric values from a specific commit.

    :param db: Database object
    :param text sha: A sha representing a single commit
    """
    results = db.execute(
        'SELECT metric_id, running_value FROM metric_data WHERE sha = ?',
        (sha,),
    )
    return dict(results)
