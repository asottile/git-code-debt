from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import flask

from git_code_debt.server import metric_config
from git_code_debt.server.presentation.commit_delta import CommitDeltaPresenter
from git_code_debt.server.presentation.delta import DeltaPresenter
from git_code_debt.server.render_mako import render_template
from git_code_debt.logic import get_metric_values
from git_code_debt.server import logic


commit = flask.Blueprint('commit', __name__)


@commit.route('/commit/<sha>')
def show(sha):
    previous_sha = logic.get_previous_sha(sha)
    if previous_sha is None:
        previous_values = collections.defaultdict(int)
    else:
        previous_values = get_metric_values(flask.g.db, previous_sha)

    values = get_metric_values(flask.g.db, sha)

    commit_deltas = sorted([
        CommitDeltaPresenter.from_data(
            metric_name,
            DeltaPresenter(
                'javascript:;',
                metric_value - previous_values[metric_name],
            ),
        )
        for metric_name, metric_value in values.items()
        if previous_values[metric_name] - metric_value
    ])

    links = [
        (link_name, link.format(sha=sha))
        for link_name, link in metric_config.commit_links
    ]

    return render_template(
        'commit.mako',
        sha=sha,
        short_sha=sha[:8],
        commit_deltas=commit_deltas,
        links=links,
    )
