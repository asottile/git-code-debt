from __future__ import absolute_import
from __future__ import unicode_literals

import flask


def test_healthcheck(server):
    server.client.get(flask.url_for('status.healthcheck'))
