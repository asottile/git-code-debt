from __future__ import annotations

import flask


status = flask.Blueprint('status', __name__)


@status.route('/status/healthcheck')
def healthcheck() -> str:
    return ''
