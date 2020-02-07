import flask

from git_code_debt.server import logic
from git_code_debt.server.presentation.commit_delta import CommitDelta
from git_code_debt.server.presentation.delta import Delta
from git_code_debt.server.render_mako import render_template


commit = flask.Blueprint('commit', __name__)


@commit.route('/commit/<sha>')
def show(sha: str) -> str:
    changes = logic.get_metric_changes(flask.g.db, sha)

    commit_deltas = sorted(
        CommitDelta.from_data(
            metric_name, Delta('javascript:;', change),
            color_overrides=flask.g.config.color_overrides,
        )
        for metric_name, change in changes
    )

    links = [
        (link_name, link.format(sha=sha))
        for link_name, link in flask.g.config.commit_links
    ]

    return render_template(
        'commit.mako',
        sha=sha,
        short_sha=sha[:8],
        commit_deltas=commit_deltas,
        links=links,
    )
