from __future__ import absolute_import
from __future__ import unicode_literals

import flask


status = flask.Blueprint('status', __name__)


@status.route('/status/healthcheck')
def healthcheck():
    return ''
