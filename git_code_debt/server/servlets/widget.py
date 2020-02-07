import json

import flask

from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.generate import get_metrics
from git_code_debt.generate_config import GenerateOptions
from git_code_debt.repo_parser import BLANK_COMMIT
from git_code_debt.server.presentation.commit_delta import CommitDelta
from git_code_debt.server.presentation.delta import Delta
from git_code_debt.server.render_mako import render_template
from git_code_debt.util import yaml


widget = flask.Blueprint('widget', __name__)


@widget.route('/widget/frame')
def frame() -> str:
    return render_template('widget_frame.mako')


@widget.route('/widget/data', methods=['POST'])
def data() -> str:
    metric_names = frozenset(flask.g.config.widget_metrics)
    diff = flask.request.form['diff'].encode('UTF-8')

    metric_config = GenerateOptions.from_yaml(
        yaml.load(open('generate_config.yaml').read()),
    )
    parsers = get_metric_parsers_from_args(
        metric_config.metric_package_names, skip_defaults=False,
    )
    metrics = get_metrics(BLANK_COMMIT, diff, parsers, metric_config.exclude)
    metrics = tuple(
        metric for metric in metrics
        if metric.value and metric.name in metric_names
    )

    commit_deltas = sorted(
        CommitDelta.from_data(
            metric.name, Delta('javascript:;', metric.value),
            color_overrides=flask.g.config.color_overrides,
        )
        for metric in metrics
    )
    return json.dumps({
        'metrics': render_template('widget.mako', commit_deltas=commit_deltas),
    })
