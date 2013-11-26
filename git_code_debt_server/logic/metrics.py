
import collections
import flask


Metric = collections.namedtuple('Metric', ['name', 'value', 'sha', 'date'])

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

def most_recent_metric(metric_name):
    result = flask.g.db.execute(
        '''
        SELECT
            running_value,
            sha,
            timestamp
        FROM metric_data
        INNER JOIN metric_names ON
            metric_names.id == metric_data.metric_id
        WHERE
            metric_names.name == ?
        ORDER BY timestamp DESC
        LIMIT 1
        ''',
        [metric_name]
    ).fetchone()

    if result:
        return Metric(metric_name, *result)
    else:
        return Metric(metric_name, 0, 'No Data', 0)

def metrics_for_dates(repo, sha, metric_name, dates):

    def get_metric_for_timestamp(timestamp):
        result = flask.g.db.execute(
            '''
            SELECT
                running_value,
                sha,
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
