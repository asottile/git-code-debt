import datetime
import flask

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.logic import metrics
from git_code_debt_util.time import to_timestamp

index = flask.Blueprint('index', __name__)

DATE_NAMES_TO_TIMEDELTAS = (
    ('Last Day', datetime.timedelta(days=1)),
    ('Last Week', datetime.timedelta(days=7)),
    ('Last Month', datetime.timedelta(days=30)),
    ('Last 3 Months', datetime.timedelta(days=90)),
    ('Last 6 Months', datetime.timedelta(days=180)),
    ('Last Year', datetime.timedelta(days=365)),
)


@index.route('/')
def show():
    metric_names = metrics.get_metric_ids_from_database()
    today = datetime.datetime.today()
    today_timestamp = to_timestamp(today)
    offsets = [
        (time_name, to_timestamp(today - offset))
        for (time_name, offset) in DATE_NAMES_TO_TIMEDELTAS
    ]
    current_values = metrics.get_metrics_for_sha(
        metrics.get_latest_sha(),
    )
    metric_data = dict(
        (
            time_name,
            metrics.get_metrics_for_sha(metrics.get_sha_for_date(timestamp)),
        )
        for (time_name, timestamp) in offsets
    )

    return render_template(
        'index.mako',
        metric_names=metric_names,
        today_timestamp=today_timestamp,
        offsets=offsets,
        current_values=current_values,
        metric_data=metric_data,
    )
