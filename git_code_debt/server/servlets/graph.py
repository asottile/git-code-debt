from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import flask
import simplejson

from git_code_debt.server import logic
from git_code_debt.server import metric_config
from git_code_debt.server.presentation.commit_delta import CommitDeltaPresenter
from git_code_debt.server.presentation.delta import DeltaPresenter
from git_code_debt.server.render_mako import render_template
from git_code_debt.util.time import data_points_for_time_range
from git_code_debt.util.time import to_timestamp


graph = flask.Blueprint('graph', __name__)


@graph.route('/graph/<metric_name>')
def show(metric_name):
    start_timestamp = int(flask.request.args.get('start'))
    end_timestamp = int(flask.request.args.get('end'))

    data_points = data_points_for_time_range(
        start_timestamp,
        end_timestamp,
        data_points=250,
    )
    metrics_for_dates = logic.metrics_for_dates(metric_name, data_points)

    metrics_for_js = sorted(set(
        (m.date * 1000, m.value)
        for m in metrics_for_dates
    ))

    changes = sorted(logic.get_major_changes_for_metric(
        flask.g.db, start_timestamp, end_timestamp, metric_name,
    ))
    changes = [
        (
            datetime.datetime.fromtimestamp(timestamp).strftime(
                '%Y-%m-%d %H:%M:%S',
            ),
            sha,
            CommitDeltaPresenter.from_data(
                metric_name,
                DeltaPresenter('javascript:;', value),
            )
        )
        for timestamp, sha, value in changes
    ]

    override_classname = (
        'color-override'
        if metric_name in metric_config.color_overrides
        else ''
    )

    return render_template(
        'graph.mako',
        metric_name=metric_name,
        metrics=simplejson.dumps(metrics_for_js),
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        changes=changes,
        override_classname=override_classname,
    )


@graph.route('/graph/<metric_name>/all_data')
def all_data(metric_name):
    earliest_timestamp = logic.get_first_data_timestamp(metric_name)
    now = datetime.datetime.today()

    return flask.redirect(flask.url_for(
        'graph.show',
        metric_name=metric_name,
        start=str(earliest_timestamp),
        end=str(to_timestamp(now)),
    ))
