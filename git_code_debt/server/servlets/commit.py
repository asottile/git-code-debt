from __future__ import absolute_import
from __future__ import unicode_literals

import flask

from git_code_debt.server import logic
from git_code_debt.server import metric_config
from git_code_debt.server.presentation.commit_delta import CommitDeltaPresenter
from git_code_debt.server.presentation.delta import DeltaPresenter
from git_code_debt.server.render_mako import render_template


commit = flask.Blueprint('commit', __name__)


@commit.route('/commit/<sha>')
def show(sha):
    changes = logic.get_metric_changes(flask.g.db, sha)

    commit_deltas = sorted([
        CommitDeltaPresenter.from_data(
            metric_name, DeltaPresenter('javascript:;', change),
        )
        for metric_name, change in changes
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
