import datetime
import json

import flask
from werkzeug.wrappers import Response

from git_code_debt.server import logic
from git_code_debt.server.render_mako import render_template
from git_code_debt.util.time import data_points_for_time_range
from git_code_debt.util.time import to_timestamp


graph = flask.Blueprint('graph', __name__)


@graph.route('/graph/<metric_name>')
def show(metric_name: str) -> str:
    start_timestamp = int(flask.request.args['start'])
    end_timestamp = int(flask.request.args['end'])

    metric_info = logic.get_metric_info(flask.g.db, metric_name)

    data_points = data_points_for_time_range(
        start_timestamp,
        end_timestamp,
        data_points=250,
    )
    metrics_for_dates = logic.metrics_for_dates(metric_info.id, data_points)

    metrics_for_js = sorted({
        (m.date * 1000, m.value) for m in metrics_for_dates
    })

    return render_template(
        'graph.mako',
        description=metric_info.description,
        metric_name=metric_name,
        metrics=json.dumps(metrics_for_js),
        start_ts=start_timestamp,
        end_ts=end_timestamp,
        changes_url=flask.url_for(
            'changes.show',
            metric_name=metric_name,
            start_ts=start_timestamp,
            end_ts=end_timestamp,
        ),
    )


@graph.route('/graph/<metric_name>/all_data')
def all_data(metric_name: str) -> Response:
    earliest_timestamp = logic.get_first_data_timestamp(metric_name)
    now = datetime.datetime.today()

    return flask.redirect(
        flask.url_for(
            'graph.show',
            metric_name=metric_name,
            start=str(earliest_timestamp),
            end=str(to_timestamp(now)),
        ),
    )
