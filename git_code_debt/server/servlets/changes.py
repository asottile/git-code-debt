from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import json

import flask

from git_code_debt.server import logic
from git_code_debt.server import metric_config
from git_code_debt.server.presentation.commit_delta import CommitDeltaPresenter
from git_code_debt.server.presentation.delta import DeltaPresenter
from git_code_debt.server.render_mako import render_template


changes = flask.Blueprint('changes', __name__)


@changes.route('/changes/<metric_name>/<start_timestamp>/<end_timestamp>')
def show(metric_name, start_timestamp, end_timestamp):
    start_timestamp = int(start_timestamp)
    end_timestamp = int(end_timestamp)

    metric_changes = sorted(logic.get_major_changes_for_metric(
        flask.g.db, start_timestamp, end_timestamp, metric_name,
    ))
    metric_changes = [
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
        for timestamp, sha, value in metric_changes
    ]

    override_classname = (
        'color-override'
        if metric_name in metric_config.color_overrides
        else ''
    )

    rendered_template = render_template(
        'changes.mako',
        changes=metric_changes,
        override_classname=override_classname,
    )

    return json.dumps({'body': rendered_template})
