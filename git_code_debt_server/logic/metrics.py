
import collections
import flask


Metric = collections.namedtuple('Metric', ['name', 'value', 'date'])


def get_metric_ids_from_database():
    result = flask.g.db.execute(
        '''
        SELECT
            name
        FROM metric_names
        ORDER BY name
        '''
    ).fetchall()
    return [name for name, in result]


def get_sha_for_date(date):
    result = flask.g.db.execute(
        '''
        SELECT
            sha
        FROM metric_data
        WHERE
            timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
        ''',
        [date],
    ).fetchone()

    # If the date is too far in the past (before data) there won't be a result
    return result[0] if result else None


def get_metrics_for_sha(sha):
    # For no sha, we default all metrics to 0
    if not sha:
        return collections.defaultdict(int)

    result = flask.g.db.execute(
        '''
        SELECT
            metric_names.name,
            metric_data.running_value
        FROM metric_data
        INNER JOIN metric_names ON
            metric_names.id = metric_data.metric_id
        WHERE
            metric_data.sha = ?
        ''',
        [sha],
    ).fetchall()

    return dict(result)


def metrics_for_dates(repo, metric_name, dates):

    def get_metric_for_timestamp(timestamp):
        result = flask.g.db.execute(
            '''
            SELECT
                running_value,
                timestamp
            FROM metric_data
            INNER JOIN metric_names ON
                metric_names.id == metric_data.metric_id
            WHERE
                metric_names.name == ? AND
                timestamp < ?
            ORDER BY timestamp DESC
            LIMIT 1
            ''',
            [metric_name, timestamp],
        ).fetchone()
        if result:
            return Metric(metric_name, *result)
        else:
            return Metric(metric_name, 0, 'No Data', date)

    return [get_metric_for_timestamp(date) for date in dates]
